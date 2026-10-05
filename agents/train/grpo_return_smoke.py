"""One GRPO step scored by the rest of a short episode.

The ledger has a 0 seat. Scripted cooperators do not name it. The zero names
the learner. The sampled action is kept for the rest of the episode, so naming
the zero, or contributing less, can change the return.
"""

from __future__ import annotations

import os
import sys

from envs.pgg_scripted.env import ScriptedPGG
from envs.pgg_scripted.run_frozen import parse_model_text, prompt_for
from envs.pgg_scripted.schema import repair


def others(ids: list[str], seat: str, zero: str) -> dict:
    actions = {}
    for sid in ids:
        if sid == seat:
            continue
        if sid == zero:
            actions[sid] = {"message": "", "nominate": [seat], "contribute": 0.0}
        else:
            actions[sid] = {
                "message": "",
                "nominate": [j for j in ids if j not in (sid, zero)],
                "contribute": 1.0,
            }
    return actions


def finish(env: ScriptedPGG, seat: str, zero: str, action: dict, rounds_left: int) -> float:
    total = 0.0
    for _ in range(rounds_left):
        actions = others(env.ids, seat, zero)
        actions[seat] = action
        contrib = {i: actions[i]["contribute"] for i in env.ids}
        noms = {i: actions[i]["nominate"] for i in env.ids}
        pay = env.payoffs(contrib, env.working)
        total += pay[seat]
        env.record(contrib, noms)
        env.working = env.form_groups(noms)
        env.last_c = contrib
    return total


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
        raise SystemExit("Use .venv-train. Fireworks needs Python 3.11+.")
    key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not key:
        raise SystemExit("FIREWORKS_API_KEY is not set. Source .env once.")
    from fireworks.training.sdk import FiretitanServiceClient
    from tinker.types.model_input import ModelInput
    from transformers import AutoTokenizer
    import tinker

    service = FiretitanServiceClient(
        api_key=key,
        base_url="https://api.fireworks.ai/training/v1/serverless",
    )
    trainer = service.create_lora_training_client(
        base_model="accounts/fireworks/models/qwen3p8-27b", rank=8
    )
    snapshot = trainer.save_weights_for_sampler("return-0002").result().path
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")
    sampler = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    ids = ["k3p9qa", "m8n2ld", "q1w4er", "z7c6vb"]
    seat, zero = ids[0], ids[-1]
    env = ScriptedPGG(ids=ids, seed=0)
    env.record(
        {seat: 1.0, ids[1]: 1.0, ids[2]: 1.0, zero: 0.0},
        {seat: [ids[1], ids[2]], ids[1]: [seat, ids[2]], ids[2]: [seat, ids[1]], zero: [seat]},
    )
    rendered = tokenizer.apply_chat_template(
        [
            {"role": "system", "content": "Reply with one JSON object only. No reasoning."},
            {"role": "user", "content": prompt_for(seat, env, ids, [])},
        ],
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )
    prompt_ids = tokenizer.encode(rendered)
    sampled = sampler.sample(
        prompt=ModelInput.from_ints(prompt_ids),
        num_samples=4,
        sampling_params={"max_tokens": 80, "temperature": 0.4},
    ).result()
    returns = []
    for sequence in sampled.sequences:
        decoded = tokenizer.decode(list(sequence.tokens))
        action, ok = repair(parse_model_text(decoded), ids)
        branch = ScriptedPGG(ids=ids, seed=0)
        branch.history = list(env.history)
        branch.working = set(env.working)
        branch.last_c = dict(env.last_c)
        value = finish(branch, seat, zero, action, rounds_left=3)
        returns.append(value)
        print(
            "reply", decoded[:120].replace("\n", " "),
            "ok", ok, "nominate", action["nominate"], "c", action["contribute"],
            "return", round(value, 3),
            flush=True,
        )
    mean = sum(returns) / len(returns)
    advantages = [value - mean for value in returns]
    print("advantages", [round(a, 3) for a in advantages], flush=True)
    if len(set(round(a, 6) for a in advantages)) == 1:
        print("no spread, skip the optimizer step", flush=True)
        sampler.close()
        return
    datums = [datum_for(prompt_ids, sequence, adv) for sequence, adv in zip(sampled.sequences, advantages)]
    trainer.forward_backward(datums, "importance_sampling").result()
    trainer.optim_step(
        tinker.AdamParams(learning_rate=2.5e-5, beta1=0.9, beta2=0.95, eps=1e-8, weight_decay=0.0)
    ).result()
    print("step_ok return-to-go", flush=True)
    sampler.close()


if __name__ == "__main__":
    main()
