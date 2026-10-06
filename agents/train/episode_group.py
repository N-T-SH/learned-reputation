"""Four complete episodes, one group. No held-fixed return.

A missing log probability aborts the step. Placebo shuffles the four returns
before the advantage. Default is two rounds, so the loop can be priced
before a 20-round run.
"""

from __future__ import annotations

import asyncio
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


def scripted(ids, probes, last):
    actions = {}
    for sid, value in probes.items():
        others = [i for i in ids if i != sid]
        actions[sid] = {
            "message": "",
            "nominate": sorted(others, key=lambda i: last[i], reverse=True)[:2],
            "contribute": value,
        }
    return actions


async def sample_one(sampler, tokenizer, prompt_ids):
    completions = await sampler.sample_with_prompt_tokens(
        prompt_ids,
        n=1,
        max_tokens=80,
        temperature=0.4,
        logprobs=True,
    )
    completion = completions[0]
    n_tokens = len(completion.full_tokens) - completion.prompt_len
    logprobs = completion.inference_logprobs
    if not logprobs or len(logprobs) < n_tokens:
        raise SystemExit("Missing log probabilities. No step.")
    return completion, logprobs[:n_tokens]


def datum_for(prompt_ids, completion_ids, logprobs, advantage):
    from tinker.types.model_input import ModelInput
    import tinker

    tokens = list(prompt_ids) + list(completion_ids)
    pad = len(prompt_ids) - 1
    return tinker.Datum(
        model_input=ModelInput.from_ints(tokens[:-1]),
        loss_fn_inputs={
            "target_tokens": tokens[1:],
            "logprobs": [0.0] * pad + list(logprobs),
            "advantages": [0.0] * pad + [advantage] * len(completion_ids),
        },
    )


def play_episode(sampler, tokenizer, ids, probes, seed, rounds):
    env = ScriptedPGG(ids=ids, seed=seed)
    records = []
    returns = {i: 0.0 for i in ids}
    for t in range(rounds):
        last = env.history[-1]["c"] if env.history else {i: 0.0 for i in ids}
        actions = scripted(ids, probes, last)
        for seat in ids:
            if seat in probes:
                continue
            text = rendered_prompt(tokenizer, seat, env, order_for(ids, seat, seed, t), [])
            prompt_ids = tokenizer.encode(text)
            completion, logprobs = asyncio.get_event_loop().run_until_complete(
                sample_one(sampler, prompt_ids)
            ) if False else None
            # filled below by the async driver
            records.append((seat, prompt_ids))
        # placeholder so the sync shape is obvious; main uses the async driver
        break
    return env, records, returns


async def episode(sampler, tokenizer, ids, probes, seed, rounds):
    env = ScriptedPGG(ids=ids, seed=seed)
    records = []
    returns = {i: 0.0 for i in ids}
    for t in range(rounds):
        last = env.history[-1]["c"] if env.history else {i: 0.0 for i in ids}
        actions = scripted(ids, probes, last)
        for seat in ids:
            if seat in probes:
                continue
            text = rendered_prompt(tokenizer, seat, env, order_for(ids, seat, seed, t), [])
            prompt_ids = tokenizer.encode(text)
            completion, logprobs = await sample_one(sampler, tokenizer, prompt_ids)
            action, ok = repair(parse_model_text(completion.text or ""), ids)
            actions[seat] = action
            completion_ids = completion.full_tokens[completion.prompt_len:]
            records.append((prompt_ids, completion_ids, logprobs))
        contrib = {i: actions[i]["contribute"] for i in ids}
        noms = {i: actions[i]["nominate"] for i in ids}
        pay = env.payoffs(contrib, env.working)
        for i in ids:
            returns[i] += pay[i]
        env.record(contrib, noms)
        env.working = env.form_groups(noms)
        env.last_c = contrib
    return records, returns


async def main_async() -> None:
    if sys.version_info < (3, 11):
        raise SystemExit("Use .venv-train. Fireworks needs Python 3.11+.")
    key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not key:
        raise SystemExit("FIREWORKS_API_KEY is not set. Source .env once.")
    placebo = "placebo" in sys.argv
    rounds = 2
    from fireworks.training.sdk import FiretitanServiceClient
    from transformers import AutoTokenizer
    import tinker

    service = FiretitanServiceClient(
        api_key=key,
        base_url="https://api.fireworks.ai/training/v1/serverless",
    )
    trainer = service.create_lora_training_client(
        base_model="accounts/fireworks/models/qwen3p8-27b", rank=8
    )
    snapshot = trainer.save_weights_for_sampler("grp-short").result().path
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")
    client = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    ids = stable_ids(8, 30)
    probes = {ids[-1]: 0.0, ids[-2]: 0.3, ids[-3]: 1.0}
    print("probes", probes, "placebo", placebo, "rounds", rounds, flush=True)
    group = []
    for g in range(4):
        records, returns = await episode(client.deployment_sampler, tokenizer, ids, probes, 30, rounds)
        group.append((records, returns))
        print("episode", g, "returns", {k: round(v, 3) for k, v in returns.items()}, flush=True)
    model = [i for i in ids if i not in probes]
    datums = []
    for seat in model:
        values = [item[1][seat] for item in group]
        order = list(values)
        if placebo:
            random.Random(0).shuffle(order)
        mean = sum(order) / len(order)
        advantages = [value - mean for value in order]
        if len(set(round(a, 6) for a in advantages)) == 1:
            print("seat", seat, "no spread", flush=True)
            continue
        for (records, _), advantage in zip(group, advantages):
            for prompt_ids, completion_ids, logprobs in records:
                datums.append(datum_for(prompt_ids, completion_ids, logprobs, advantage))
        print("seat", seat, "advantages", [round(a, 3) for a in advantages], flush=True)
    if not datums:
        print("no step", flush=True)
    else:
        trainer.forward_backward(datums, "importance_sampling").result()
        trainer.optim_step(
            tinker.AdamParams(learning_rate=1e-5, beta1=0.9, beta2=0.95, eps=1e-8, weight_decay=0.0)
        ).result()
        print("step_ok", "placebo" if placebo else "payoff", "datums", len(datums), flush=True)
    client.close()


if __name__ == "__main__":
    asyncio.run(main_async())
