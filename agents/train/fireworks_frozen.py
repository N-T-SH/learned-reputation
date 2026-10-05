"""Frozen Fireworks file. Same rendered prompt as the pilot. No optimizer step.

One reply per model seat. This is the before picture for a Fireworks pilot.
The OpenRouter file is a different endpoint and is not this comparison.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from agents.train.prompt import rendered_prompt
from envs.pgg_scripted.env import ScriptedPGG
from envs.pgg_scripted.run_frozen import episode_ids, order_for, parse_model_text
from envs.pgg_scripted.schema import repair


def main() -> None:
    if sys.version_info < (3, 11):
        raise SystemExit("Use .venv-train. Fireworks needs Python 3.11+.")
    key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not key:
        raise SystemExit("FIREWORKS_API_KEY is not set. Source .env once.")
    from fireworks.training.sdk import FiretitanServiceClient
    from tinker.types.model_input import ModelInput
    from transformers import AutoTokenizer

    service = FiretitanServiceClient(
        api_key=key,
        base_url="https://api.fireworks.ai/training/v1/serverless",
    )
    trainer = service.create_lora_training_client(
        base_model="accounts/fireworks/models/qwen3p8-27b", rank=8
    )
    snapshot = trainer.save_weights_for_sampler("frozen-0001").result().path
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")
    sampler = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    ids = episode_ids(8, 0)
    probes = {ids[-1]: 0.0, ids[-2]: 0.3}
    env = ScriptedPGG(ids=ids, seed=0)
    path = Path("runs/train/fireworks_frozen_seed0.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    for t in range(5):
        actions, oks = {}, {}
        for seat, value in probes.items():
            last = env.history[-1]["c"] if env.history else {i: 0.0 for i in ids}
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
            text = rendered_prompt(tokenizer, seat, env, order_for(ids, seat, 0, t), [])
            sampled = sampler.sample(
                prompt=ModelInput.from_ints(tokenizer.encode(text)),
                num_samples=1,
                sampling_params={"max_tokens": 80, "temperature": 0.4},
            ).result()
            decoded = tokenizer.decode(list(sampled.sequences[0].tokens))
            action, ok = repair(parse_model_text(decoded), ids)
            actions[seat], oks[seat] = action, ok
            print("t", t, "seat", seat, "ok", ok, "c", action["contribute"], "nom", action["nominate"], flush=True)
        row = {
            "t": t,
            "prompt": "fireworks-chat",
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
    print("wrote", path, flush=True)
    sampler.close()


if __name__ == "__main__":
    main()
