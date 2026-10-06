"""Two-round group, then one measurement episode. No further step.

Usage: python -m agents.train.group_then_measure payoff
       python -m agents.train.group_then_measure placebo
"""

from __future__ import annotations

import asyncio
import json
import os
import random
import string
import sys
from pathlib import Path

from agents.train.episode_group import datum_for, episode, stable_ids
from agents.train.prompt import rendered_prompt
from envs.pgg_scripted.env import ScriptedPGG
from envs.pgg_scripted.run_frozen import order_for, parse_model_text
from envs.pgg_scripted.schema import repair


async def measure(sampler, tokenizer, ids, probes, seed, path: Path):
    env = ScriptedPGG(ids=ids, seed=seed)
    for t in range(2):
        last = env.history[-1]["c"] if env.history else {i: 0.0 for i in ids}
        actions, oks = {}, {}
        for seat, value in probes.items():
            others = [i for i in ids if i != seat]
            actions[seat] = {
                "message": "",
                "nominate": sorted(others, key=lambda i: last[i], reverse=True)[:2],
                "contribute": value,
            }
            oks[seat] = True
        for seat in ids:
            if seat in probes:
                continue
            text = rendered_prompt(tokenizer, seat, env, order_for(ids, seat, seed, t), [])
            prompt_ids = tokenizer.encode(text)
            completions = await sampler.sample_with_prompt_tokens(
                prompt_ids, n=1, max_tokens=80, temperature=0.4, logprobs=True
            )
            action, ok = repair(parse_model_text(completions[0].text or ""), ids)
            actions[seat], oks[seat] = action, ok
        row = {"t": t, "seed": seed, "probes": probes, "ok": oks, "action": actions}
        with path.open("a") as handle:
            handle.write(json.dumps(row) + "\n")
        contrib = {i: actions[i]["contribute"] for i in ids}
        noms = {i: actions[i]["nominate"] for i in ids}
        env.record(contrib, noms)
        env.working = env.form_groups(noms)
        env.last_c = contrib
        print("measure", seed, "t", t, "noms", {s: actions[s]["nominate"] for s in ids if s not in probes}, flush=True)


async def main_async() -> None:
    if sys.version_info < (3, 11):
        raise SystemExit("Use .venv-train.")
    kind = sys.argv[1] if len(sys.argv) > 1 else ""
    if kind not in {"payoff", "placebo"}:
        raise SystemExit("Use payoff or placebo.")
    key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not key:
        raise SystemExit("FIREWORKS_API_KEY is not set. Source .env once.")
    from fireworks.training.sdk import FiretitanServiceClient
    from transformers import AutoTokenizer
    import tinker

    path = Path(f"runs/train/group_measure_{kind}.jsonl")
    if path.exists():
        raise SystemExit(f"{path} already exists.")
    path.parent.mkdir(parents=True, exist_ok=True)
    service = FiretitanServiceClient(
        api_key=key,
        base_url="https://api.fireworks.ai/training/v1/serverless",
    )
    trainer = service.create_lora_training_client(
        base_model="accounts/fireworks/models/qwen3p8-27b", rank=8
    )
    snapshot = trainer.save_weights_for_sampler(f"gm-{kind[:4]}").result().path
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")
    client = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    ids = stable_ids(8, 31)
    probes = {ids[-1]: 0.0, ids[-2]: 0.3, ids[-3]: 1.0}
    group = []
    for _ in range(4):
        group.append(await episode(client.deployment_sampler, tokenizer, ids, probes, 31, 2))
    datums = []
    for seat in ids:
        if seat in probes:
            continue
        values = [item[1][seat] for item in group]
        scored = list(values)
        if kind == "placebo":
            random.Random(0).shuffle(scored)
        mean = sum(scored) / len(scored)
        advantages = [value - mean for value in scored]
        if len(set(round(a, 6) for a in advantages)) == 1:
            continue
        for (records, _), advantage in zip(group, advantages):
            for owner, prompt_ids, completion_ids, logprobs in records:
                if owner == seat:
                    datums.append(datum_for(prompt_ids, completion_ids, logprobs, advantage))
    if datums:
        trainer.forward_backward(datums, "importance_sampling").result()
        trainer.optim_step(
            tinker.AdamParams(learning_rate=1e-5, beta1=0.9, beta2=0.95, eps=1e-8, weight_decay=0.0)
        ).result()
        client.close()
        snapshot = trainer.save_weights_for_sampler(f"gm-{kind[:4]}-s").result().path
        client = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    print("step", kind, "datums", len(datums), flush=True)
    await measure(client.deployment_sampler, tokenizer, ids, probes, 31, path)
    print("wrote", path, flush=True)
    client.close()


if __name__ == "__main__":
    asyncio.run(main_async())
