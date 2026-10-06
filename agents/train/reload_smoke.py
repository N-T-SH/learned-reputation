"""Sample once from a saved snapshot in a fresh process. No optimizer step.

A 404 means the measurement has to stay in the process that saved the adapter.
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path


def main() -> None:
    if sys.version_info < (3, 11):
        raise SystemExit("Use .venv-train.")
    key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not key:
        raise SystemExit("FIREWORKS_API_KEY is not set. Source .env once.")
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "runs/train/adapter_r20.txt")
    if not path.exists():
        raise SystemExit(f"No snapshot file at {path}.")
    snapshot = path.read_text().strip()
    from fireworks.training.sdk import FiretitanServiceClient
    from transformers import AutoTokenizer

    service = FiretitanServiceClient(
        api_key=key,
        base_url="https://api.fireworks.ai/training/v1/serverless",
    )
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")
    client = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    prompt_ids = tokenizer.encode("Reply with a JSON object with keys message, nominate, contribute.")

    async def once():
        return await client.deployment_sampler.sample_with_prompt_tokens(
            prompt_ids, n=1, max_tokens=20, temperature=0.4, logprobs=True
        )

    try:
        completions = asyncio.run(once())
    except Exception as exc:
        raise SystemExit(f"reload_failed {type(exc).__name__}: {exc}") from exc
    text = (completions[0].text or "").replace("\n", " ")[:80]
    print("reload_ok", snapshot, "text", text, flush=True)
    client.close()


if __name__ == "__main__":
    main()
