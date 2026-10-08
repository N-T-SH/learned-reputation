"""Frozen episode on the long-run ids. No optimizer step.

Seed 40 matches runs/train/long_payoff.jsonl. Prints selectivity.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

from agents.train.episode_group import stable_ids
from agents.train.long_group import measure, selectivity
from fireworks.training.sdk import FiretitanServiceClient
from transformers import AutoTokenizer


async def main_async() -> None:
    if sys.version_info < (3, 11):
        raise SystemExit("Use .venv-train.")
    key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not key:
        raise SystemExit("FIREWORKS_API_KEY is not set. Source .env once.")
    path = Path("runs/train/long_frozen_seed40.jsonl")
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
    snapshot = trainer.save_weights_for_sampler("frz-40").result().path
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")
    client = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    ids = stable_ids(8, 40)
    probes = {ids[-1]: 0.0, ids[-2]: 0.3, ids[-3]: 1.0}
    print("frozen seed 40 probes", probes, flush=True)
    await measure(client.deployment_sampler, tokenizer, ids, probes, 40, path)
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    n0, n1, decisions, breadth = selectivity(rows, probes)
    fails = sum(1 for row in rows for seat, ok in row["ok"].items() if seat not in probes and not ok)
    print("repair_failures", fails, "of", decisions, flush=True)
    print("wrote", path, flush=True)
    client.close()


if __name__ == "__main__":
    asyncio.run(main_async())
