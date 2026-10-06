"""One sample with logprobs requested. No optimizer step.

The last training loop filled missing log probabilities with zeros. This
refuses to continue unless the sampler returns a list matching the completion.
"""

from __future__ import annotations

import asyncio
import os
import sys

from agents.train.prompt import rendered_prompt
from envs.pgg_scripted.env import ScriptedPGG
from envs.pgg_scripted.run_frozen import order_for


def main() -> None:
    if sys.version_info < (3, 11):
        raise SystemExit("Use .venv-train. Fireworks needs Python 3.11+.")
    key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not key:
        raise SystemExit("FIREWORKS_API_KEY is not set. Source .env once.")
    from fireworks.training.sdk import FiretitanServiceClient
    from transformers import AutoTokenizer

    service = FiretitanServiceClient(
        api_key=key,
        base_url="https://api.fireworks.ai/training/v1/serverless",
    )
    trainer = service.create_lora_training_client(
        base_model="accounts/fireworks/models/qwen3p8-27b", rank=8
    )
    snapshot = trainer.save_weights_for_sampler("lp-smoke").result().path
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")
    client = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    ids = ["aaaaaa", "bbbbbb", "cccccc", "dddddd", "eeeeee", "ffffff", "gggggg", "hhhhhh"]
    env = ScriptedPGG(ids=ids, seed=0)
    text = rendered_prompt(tokenizer, ids[0], env, order_for(ids, ids[0], 0, 0), [])
    prompt_ids = tokenizer.encode(text)

    async def once():
        return await client.deployment_sampler.sample_with_prompt_tokens(
            prompt_ids,
            n=1,
            max_tokens=40,
            temperature=0.4,
            logprobs=True,
        )

    completions = asyncio.run(once())
    completion = completions[0]
    logprobs = getattr(completion, "inference_logprobs", None)
    n_tokens = len(completion.full_tokens) - completion.prompt_len
    print("text", (completion.text or "")[:120].replace("\n", " "), flush=True)
    print("completion_tokens", n_tokens, "logprobs", None if logprobs is None else len(logprobs), flush=True)
    if not logprobs or len(logprobs) < n_tokens:
        raise SystemExit("No usable log probabilities. Do not train.")
    print("logprob_head", [round(x, 3) for x in logprobs[:4]], flush=True)
    print("logprob_smoke_ok", flush=True)
    client.close()


if __name__ == "__main__":
    main()
