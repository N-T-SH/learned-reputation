"""One GRPO step on Fireworks serverless. Not the study pilot.

Install with uv into .venv-train on Python 3.11. Needs FIREWORKS_API_KEY.
The sampler takes token ids, not a string. This smoke stops after one sample.
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
        from tinker.types.model_input import ModelInput
    except ImportError as exc:
        raise SystemExit(
            "uv pip install 'fireworks-ai[training]>=1.2.11,<2' transformers"
        ) from exc
    try:
        from transformers import AutoTokenizer
    except ImportError as exc:
        raise SystemExit("uv pip install transformers") from exc

    base = "accounts/fireworks/models/qwen3p8-27b"
    service = FiretitanServiceClient(
        api_key=key,
        base_url="https://api.fireworks.ai/training/v1/serverless",
    )
    trainer = service.create_lora_training_client(base_model=base, rank=8)
    print("session", service.training_session_id, "run", trainer.run_id, flush=True)
    snapshot = trainer.save_weights_for_sampler("smoke-0001").result().path
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")
    sampler = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    text = (
        "Reply with one JSON object only. Keys: message, nominate, contribute. "
        "contribute is a number from 0 to 1. No reasoning."
    )
    prompt = ModelInput.from_ints(tokenizer.encode(text))
    sampled = sampler.sample(
        prompt=prompt,
        num_samples=4,
        sampling_params={"max_tokens": 80, "temperature": 0.4},
    ).result()
    print("sample_type", type(sampled).__name__, flush=True)
    print("sample_head", str(sampled)[:800], flush=True)
    sampler.close()
    print("smoke reached a sample. Datum step is next once this shape is known.", flush=True)


if __name__ == "__main__":
    main()
