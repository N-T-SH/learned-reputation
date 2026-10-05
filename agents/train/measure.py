"""Train one episode, then measure three frozen and three trained episodes.

Measurement episodes do not take an optimizer step. The trained measurement
reads the snapshot path written by the train run. Ids are new each episode.
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


def one_episode(sampler, tokenizer, ids: list[str], probes: dict[str, float], seed: int, path: Path) -> None:
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


def measure(kind: str, snapshot: str) -> None:
    from fireworks.training.sdk import FiretitanServiceClient
    from transformers import AutoTokenizer

    key = os.environ["FIREWORKS_API_KEY"].strip()
    service = FiretitanServiceClient(
        api_key=key,
        base_url="https://api.fireworks.ai/training/v1/serverless",
    )
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")
    sampler = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    path = Path(f"runs/train/measure_{kind}.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise SystemExit(f"{path} already exists. Refusing to append.")
    seeds = [1, 2, 3] if kind == "frozen" else [4, 5, 6]
    for seed in seeds:
        ids = stable_ids(8, seed)
        probes = {ids[-1]: 0.0, ids[-2]: 0.3}
        print("kind", kind, "seed", seed, "probes", probes, flush=True)
        one_episode(sampler, tokenizer, ids, probes, seed, path)
    print("wrote", path, flush=True)
    sampler.close()


def main() -> None:
    if sys.version_info < (3, 11):
        raise SystemExit("Use .venv-train. Fireworks needs Python 3.11+.")
    if not os.environ.get("FIREWORKS_API_KEY", "").strip():
        raise SystemExit("FIREWORKS_API_KEY is not set. Source .env once.")
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "frozen":
        from fireworks.training.sdk import FiretitanServiceClient

        service = FiretitanServiceClient(
            api_key=os.environ["FIREWORKS_API_KEY"].strip(),
            base_url="https://api.fireworks.ai/training/v1/serverless",
        )
        trainer = service.create_lora_training_client(
            base_model="accounts/fireworks/models/qwen3p8-27b", rank=8
        )
        snapshot = trainer.save_weights_for_sampler("base-r20").result().path
        measure("frozen", snapshot)
        return
    if mode == "trained":
        saved = Path("runs/train/adapter_r20.txt")
        if not saved.exists():
            raise SystemExit("No adapter_r20.txt. Train an episode and save the snapshot path first.")
        measure("trained", saved.read_text().strip())
        return
    raise SystemExit("Use: python -m agents.train.measure frozen   or   python -m agents.train.measure trained")


if __name__ == "__main__":
    main()
