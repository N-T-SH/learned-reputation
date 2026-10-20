"""20 Oct v2 game runs. Rules in the prompt. partners key. Stable ids.

Usage:
  python -m agents.probes.oct20_game --check
  python -m agents.probes.oct20_game --arm window --seed 0

Parse gate: run window seed 0 first. Stop if more than 15 of the first 50 fail.
Files end in _v2. The 20 Oct files are not touched.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from agents.train.parse_reply import parse_reply
from agents.train.prompt import RULES, rendered_prompt_v2, v2_body
from envs.pgg_scripted.env import ScriptedPGG
from envs.pgg_scripted.run_frozen import episode_ids_stable, order_for, scripted_action
from envs.pgg_scripted.schema import repair

ARMS = {
    "recency": {"memory": 1, "groups": "choice"},
    "window": {"memory": 5, "groups": "choice"},
    "full": {"memory": 24, "groups": "choice"},
    "fixed": {"memory": 5, "groups": "fixed"},
}
FORBIDDEN = ("cooperate", "defect", "public goods", "reputation", "trust", "punishment", "free rider")


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
    ids = episode_ids_stable(8, 40 + seed)
    reformer, steady, zero = ids[-3], ids[-2], ids[-1]
    env = ScriptedPGG(ids=ids, seed=seed, ledger=spec["memory"])
    path = Path(f"runs/oct20/game/{arm}_s{seed}_v2.jsonl")
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
            prompt = rendered_prompt_v2(
                tokenizer, seat, env, order_for(ids, seat, seed, t),
                extra="Play may end after any round.",
            )
            raw = await one_reply(sampler, tokenizer, prompt)
            parsed = parse_reply(raw)
            kind = repair_kind(parsed)
            if kind == "ok":
                action, ok = repair(parsed, ids)
                if not ok:
                    kind = "unknown id"
            else:
                action, ok = repair(parsed, ids)
            actions[seat], oks[seat], kinds[seat], texts[seat] = action, ok, kind, raw
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
            "text": texts,
            "working": sorted(env.working),
            "v2": True,
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
    return path


def check() -> None:
    low = RULES.lower()
    hit = [word for word in FORBIDDEN if word in low]
    if hit:
        raise SystemExit(f"forbidden words in rules: {hit}")
    print("word_check_ok")
    here = episode_ids_stable(8, 40)
    other = subprocess.check_output(
        [sys.executable, "-c", "from envs.pgg_scripted.run_frozen import episode_ids_stable; print(episode_ids_stable(8, 40))"],
        text=True,
    ).strip()
    if str(here) != other:
        raise SystemExit(f"id order differs across processes: {here} vs {other}")
    print("ids_stable", here)
    for arm, spec in ARMS.items():
        ids = episode_ids_stable(8, 40)
        env = ScriptedPGG(ids=ids, seed=0, ledger=spec["memory"])
        for t in range(3):
            env.record({i: 1.0 for i in ids}, {i: [] for i in ids})
        body = v2_body(ids[0], env, order_for(ids, ids[0], 0, 2), extra="Play may end after any round.")
        print(f"\n===== {arm} round 3 =====")
        print(body)
    print("\ncheck_ok")


async def main_async():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--arm", choices=list(ARMS))
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    if args.check:
        check()
        return
    if args.arm is None or args.seed is None:
        raise SystemExit("Use --check, or --arm and --seed.")
    if sys.version_info < (3, 11):
        raise SystemExit("Use .venv-train.")
    key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not key:
        raise SystemExit("FIREWORKS_API_KEY is not set.")
    from fireworks.training.sdk import FiretitanServiceClient
    from transformers import AutoTokenizer

    service = FiretitanServiceClient(api_key=key, base_url="https://api.fireworks.ai/training/v1/serverless")
    trainer = service.create_lora_training_client(base_model="accounts/fireworks/models/qwen3p8-27b", rank=8)
    snapshot = trainer.save_weights_for_sampler(f"v2-{args.arm[:4]}-{args.seed}").result().path
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")
    client = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    await episode(client.deployment_sampler, tokenizer, args.arm, args.seed)
    client.close()
    spend = Path("runs/oct20/spend.jsonl")
    with spend.open("a") as handle:
        handle.write(json.dumps({"step": "game-v2", "arm": args.arm, "seed": args.seed, "calls": 120}) + "\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main_async())
