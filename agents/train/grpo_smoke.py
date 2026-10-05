"""One GRPO step on Fireworks serverless. Not the study pilot.

A reply scores 1 only if the text itself is a JSON object with contribute.
Advantages are the group mean subtracted from that score. One step if they differ.
"""

from __future__ import annotations

import json
import os
import sys


def score(text: str) -> float:
    raw = text.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.removeprefix("json").strip()
    if not raw.startswith("{"):
        return 0.0
    try:
        parsed = json.loads(raw[: raw.rfind("}") + 1])
    except json.JSONDecodeError:
        return 0.0
    return 1.0 if isinstance(parsed, dict) and "contribute" in parsed else 0.0


def datum_for(prompt_ids: list[int], sequence, advantage: float):
    from tinker.types.model_input import ModelInput
    import tinker

    completion = list(sequence.tokens)
    logprobs = list(sequence.logprobs or [0.0] * len(completion))
    if len(logprobs) != len(completion):
        logprobs = [0.0] * len(completion)
    tokens = prompt_ids + completion
    pad = len(prompt_ids) - 1
    return tinker.Datum(
        model_input=ModelInput.from_ints(tokens[:-1]),
        loss_fn_inputs={
            "target_tokens": tokens[1:],
            "logprobs": [0.0] * pad + logprobs,
            "advantages": [0.0] * pad + [advantage] * len(completion),
        },
    )


def main() -> None:
    if sys.version_info < (3, 11):
        raise SystemExit("Fireworks training SDK needs Python 3.11+. This interpreter is older.")
    key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not key:
        raise SystemExit("FIREWORKS_API_KEY is not set. Add it to .env and source once.")
    from fireworks.training.sdk import FiretitanServiceClient
    from tinker.types.model_input import ModelInput
    from transformers import AutoTokenizer
    import tinker

    base = "accounts/fireworks/models/qwen3p8-27b"
    service = FiretitanServiceClient(
        api_key=key,
        base_url="https://api.fireworks.ai/training/v1/serverless",
    )
    trainer = service.create_lora_training_client(base_model=base, rank=8)
    print("session", service.training_session_id, "run", trainer.run_id, flush=True)
    snapshot = trainer.save_weights_for_sampler("smoke-0003").result().path
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")
    sampler = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    messages = [
        {"role": "system", "content": "Reply with one JSON object only. No reasoning."},
        {
            "role": "user",
            "content": "Keys: message, nominate, contribute. contribute is a number from 0 to 1.",
        },
    ]
    rendered = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
    )
    prompt_ids = tokenizer.encode(rendered)
    sampled = sampler.sample(
        prompt=ModelInput.from_ints(prompt_ids),
        num_samples=4,
        sampling_params={"max_tokens": 80, "temperature": 0.4},
    ).result()
    rewards = []
    for sequence in sampled.sequences:
        decoded = tokenizer.decode(list(sequence.tokens))
        rewards.append(score(decoded))
        print("reply", decoded[:180].replace("\n", " "), "score", rewards[-1], flush=True)
    mean = sum(rewards) / len(rewards)
    advantages = [reward - mean for reward in rewards]
    print("advantages", advantages, flush=True)
    if len(set(round(a, 6) for a in advantages)) == 1:
        print("no spread, skip the optimizer step", flush=True)
        sampler.close()
        return
    datums = [
        datum_for(prompt_ids, sequence, adv)
        for sequence, adv in zip(sampled.sequences, advantages)
    ]
    trained = trainer.forward_backward(datums, "importance_sampling").result()
    trainer.optim_step(
        tinker.AdamParams(learning_rate=2.5e-5, beta1=0.9, beta2=0.95, eps=1e-8, weight_decay=0.0)
    ).result()
    print("step_ok", type(trained).__name__, flush=True)
    sampler.close()


if __name__ == "__main__":
    main()
