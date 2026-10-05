"""One GRPO step on Fireworks serverless. Not the study pilot.

Needs Python 3.11+ and FIREWORKS_API_KEY. The reward here is a stand-in:
a parsed JSON reply scores 1, anything else scores 0. The study reward is
the seat's return from that round to the end of the episode.
"""

from __future__ import annotations

import os
import sys


def main() -> None:
    if sys.version_info < (3, 11):
        raise SystemExit("Fireworks training SDK needs Python 3.11+. This interpreter is older.")
    key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not key:
        raise SystemExit("FIREWORKS_API_KEY is not set. Add it to .env and source once.")
    try:
        from fireworks.training.sdk import FiretitanServiceClient
    except ImportError as exc:
        raise SystemExit("pip install 'fireworks-ai[training]>=1.2.11,<2'") from exc

    base = "accounts/fireworks/models/qwen3p8-27b"
    service = FiretitanServiceClient(
        api_key=key,
        base_url="https://api.fireworks.ai/training/v1/serverless",
    )
    trainer = service.create_lora_training_client(base_model=base, rank=8)
    print("session", service.training_session_id, "run", trainer.run_id, flush=True)
    snapshot = trainer.save_weights_for_sampler("smoke-0001").result().path
    sampler = service.create_sampling_client(model_path=snapshot)
    prompt = (
        "Reply with one JSON object only. Keys: message, nominate, contribute. "
        "contribute is a number from 0 to 1. No reasoning."
    )
    sampled = sampler.sample(
        prompt=prompt,
        num_samples=4,
        sampling_params={"max_tokens": 80, "temperature": 0.4},
    ).result()
    print("sample_type", type(sampled).__name__, flush=True)
    print("sample_head", str(sampled)[:500], flush=True)
    sampler.close()
    print("smoke reached a sample. Datum step is next once this shape is known.", flush=True)


if __name__ == "__main__":
    main()
