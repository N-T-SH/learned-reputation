"""20 Oct game runs. Memory window and a scripted reformer. No training.

Usage:
  python -m agents.probes.oct20_game --arm window --seed 0
  python -m agents.probes.oct20_game --arm recency --seed 1
  python -m agents.probes.oct20_game --arm full --seed 0
  python -m agents.probes.oct20_game --arm fixed --seed 0

Parse gate: run window seed 0 first. Stop if more than 15 of the first 50 fail.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from agents.train.parse_reply import parse_reply
from agents.train.prompt import rendered_prompt
from envs.pgg_scripted.env import ScriptedPGG
from envs.pgg_scripted.run_frozen import episode_ids, order_for, scripted_action
from envs.pgg_scripted.schema import repair

ARMS = {
    "recency": {"memory": 1, "groups": "choice"},
    "window": {"memory": 5, "groups": "choice"},
    "full": {"memory": 24, "groups": "choice"},
    "fixed": {"memory": 5, "groups": "fixed"},
}


def reformer_action(env, seat, t):
    value = 0.0 if t < 8 else 1.0
    return scripted_action(env, seat, value)


def repair_kind(raw) -> str:
    if raw is None or raw == "":
        return "empty"
    if not isinstance(raw, dict):
        return "non-JSON"
    return "ok"


async def one_reply(sampler, tokenizer, prompt):
    completions = await sampler.sample_with_prompt_tokens(
        tokenizer.encode(prompt), n=1, max_tokens=160, temperature=0.4, logprobs=False
    )
    return completions[0].text or ""


async def episode(sampler, tokenizer, arm, seed):
    spec = ARMS[arm]
    ids = episode_ids(8, 40 + seed)
    reformer, steady, zero = ids[-3], ids[-2], ids[-1]
    env = ScriptedPGG(ids=ids, seed=seed, ledger=spec["memory"])
    path = Path(f"runs/oct20/game/{arm}_s{seed}.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    fails = 0
    for t in range(24):
        actions, oks, kinds, texts = {}, {}, {}, {}
        actions[reformer] = reformer_action(env, reformer, t)
        actions[steady] = scripted_action(env, steady, 1.0)
        actions[zero] = scripted_action(env, zero, 0.0)
        for seat in (reformer, steady, zero):
            oks[seat], kinds[seat], texts[seat] = True, "scripted", ""
        for seat in ids:
            if seat in (reformer, steady, zero):
                continue
            prompt = rendered_prompt(tokenizer, seat, env, order_for(ids, seat, seed, t), [])
            prompt += "\nPlay may end after any round."
            raw = await one_reply(sampler, tokenizer, prompt)
            parsed = parse_reply(raw)
            kind = repair_kind(parsed)
            if kind == "ok":
                action, ok = repair(parsed, ids)
                if not ok:
                    kind = "unknown id" if any(n not in ids for n in parsed.get("nominate", []) if isinstance(parsed.get("nominate"), list)) else "non-JSON"
            else:
                action, ok = repair(parsed, ids)
            actions[seat], oks[seat], kinds[seat], texts[seat] = action, ok, kind, raw[:160]
            if not ok:
                fails += 1
        if arm == "window" and seed == 0 and t == 9 and fails > 15:
            raise SystemExit(f"parse gate failed: {fails} of first 50. Stop the game runs.")
        row = {
            "t": t,
            "seed": seed,
            "arm": arm,
            "memory": spec["memory"],
            "groups": spec["groups"],
            "ids": ids,
            "reformer": reformer,
            "steady": steady,
            "zero": zero,
            "ok": oks,
            "repair": kinds,
            "action": actions,
            "text_head": texts,
            "working": sorted(env.working),
        }
        with path.open("a") as handle:
            handle.write(json.dumps(row) + "\n")
        contrib = {i: actions[i]["contribute"] for i in ids}
        noms = {i: actions[i]["nominate"] for i in ids}
        env.record(contrib, noms)
        env.working = set(ids) if spec["groups"] == "fixed" else env.form_groups(noms)
        env.last_c = contrib
        print(arm, "seed", seed, "t", t, "fails", fails, flush=True)
    print("wrote", path, "fails", fails, flush=True)


async def main_async():
    if sys.version_info < (3, 11):
        raise SystemExit("Use .venv-train.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--arm", choices=list(ARMS), required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not key:
        raise SystemExit("FIREWORKS_API_KEY is not set.")
    from fireworks.training.sdk import FiretitanServiceClient
    from transformers import AutoTokenizer

    service = FiretitanServiceClient(api_key=key, base_url="https://api.fireworks.ai/training/v1/serverless")
    trainer = service.create_lora_training_client(base_model="accounts/fireworks/models/qwen3p8-27b", rank=8)
    snapshot = trainer.save_weights_for_sampler(f"g-{args.arm[:4]}-{args.seed}").result().path
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")
    client = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    await episode(client.deployment_sampler, tokenizer, args.arm, args.seed)
    client.close()
    spend = Path("runs/oct20/spend.jsonl")
    with spend.open("a") as handle:
        handle.write(json.dumps({"step": "game", "arm": args.arm, "seed": args.seed, "calls": 120}) + "\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main_async())
