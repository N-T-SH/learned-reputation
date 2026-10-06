"""Control: a scripted seat that contributes 1, beside the 0 and 0.3 probes.

Eight seats, five model seats. No optimizer step. Frozen uses a fresh adapter.
Trained tries the saved snapshot on the same session. A second client 404s.
"""

from __future__ import annotations

import json
import os
import random
import string
import sys
from pathlib import Path

from agents.train.prompt import rendered_prompt
from envs.pgg_scripted.env import ScriptedPGG
from envs.pgg_scripted.run_frozen import order_for, parse_model_text
from envs.pgg_scripted.schema import repair


def stable_ids(n: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    alphabet = string.ascii_lowercase + string.digits
    ids = []
    while len(ids) < n:
        label = "".join(rng.choice(alphabet) for _ in range(6))
        if label not in ids:
            ids.append(label)
    return ids


def probes_for(ids: list[str]) -> dict[str, float]:
    return {ids[-1]: 0.0, ids[-2]: 0.3, ids[-3]: 1.0}


def one_episode(sampler, tokenizer, ids, probes, seed, path) -> None:
    from tinker.types.model_input import ModelInput

    env = ScriptedPGG(ids=ids, seed=seed)
    for t in range(20):
        actions, oks = {}, {}
        last = env.history[-1]["c"] if env.history else {i: 0.0 for i in ids}
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
            sampled = sampler.sample(
                prompt=ModelInput.from_ints(tokenizer.encode(text)),
                num_samples=1,
                sampling_params={"max_tokens": 80, "temperature": 0.4},
            ).result()
            decoded = tokenizer.decode(list(sampled.sequences[0].tokens))
            action, ok = repair(parse_model_text(decoded), ids)
            actions[seat], oks[seat] = action, ok
        row = {
            "t": t,
            "seed": seed,
            "ids": ids,
            "probes": probes,
            "ok": oks,
            "working": sorted(env.working),
            "action": actions,
        }
        with path.open("a") as handle:
            handle.write(json.dumps(row) + "\n")
        contrib = {i: actions[i]["contribute"] for i in ids}
        noms = {i: actions[i]["nominate"] for i in ids}
        env.record(contrib, noms)
        env.working = env.form_groups(noms)
        env.last_c = contrib
        print("seed", seed, "t", t, "working", len(env.working), flush=True)


def main() -> None:
    if sys.version_info < (3, 11):
        raise SystemExit("Use .venv-train. Fireworks needs Python 3.11+.")
    key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not key:
        raise SystemExit("FIREWORKS_API_KEY is not set. Source .env once.")
    kind = sys.argv[1] if len(sys.argv) > 1 else "frozen"
    if kind not in {"frozen", "trained"}:
        raise SystemExit("Use: python -m agents.train.control_high frozen   or   trained")
    from fireworks.training.sdk import FiretitanServiceClient
    from transformers import AutoTokenizer

    path = Path(f"runs/train/control_high_{kind}.jsonl")
    if path.exists():
        raise SystemExit(f"{path} already exists. Refusing to append.")
    path.parent.mkdir(parents=True, exist_ok=True)
    service = FiretitanServiceClient(
        api_key=key,
        base_url="https://api.fireworks.ai/training/v1/serverless",
    )
    trainer = service.create_lora_training_client(
        base_model="accounts/fireworks/models/qwen3p8-27b", rank=8
    )
    if kind == "frozen":
        snapshot = trainer.save_weights_for_sampler("ctrl-base").result().path
        seeds = (21, 22, 23)
    else:
        saved = Path("runs/train/adapter_r20.txt")
        if not saved.exists():
            raise SystemExit("No adapter_r20.txt.")
        snapshot = saved.read_text().strip()
        seeds = (24, 25, 26)
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")
    sampler = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    for seed in seeds:
        ids = stable_ids(8, seed)
        probes = probes_for(ids)
        print("kind", kind, "seed", seed, "probes", probes, flush=True)
        one_episode(sampler, tokenizer, ids, probes, seed, path)
    print("wrote", path, flush=True)
    sampler.close()


if __name__ == "__main__":
    main()
