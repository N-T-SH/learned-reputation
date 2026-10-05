"""Train one 20-round episode, then measure three episodes with no further steps.

The measurement uses the same session as the save. A new client 404s.
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


def hold_return(env, actions, seat, rounds_left):
    branch = ScriptedPGG(ids=list(env.ids), seed=0)
    branch.history = list(env.history)
    branch.working = set(env.working)
    branch.last_c = dict(env.last_c)
    total = 0.0
    for _ in range(rounds_left):
        contrib = {i: actions[i]["contribute"] for i in branch.ids}
        noms = {i: actions[i]["nominate"] for i in branch.ids}
        total += branch.payoffs(contrib, branch.working)[seat]
        branch.record(contrib, noms)
        branch.working = branch.form_groups(noms)
        branch.last_c = contrib
    return total


def datum_for(prompt_ids, sequence, advantage):
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


def measure(sampler, tokenizer, path: Path) -> None:
    from tinker.types.model_input import ModelInput

    for seed in (14, 15, 16):
        ids = stable_ids(8, seed)
        probes = {ids[-1]: 0.0, ids[-2]: 0.3}
        print("measure", seed, "probes", probes, flush=True)
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
            print("measure", seed, "t", t, "working", len(env.working), flush=True)


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

    out = Path("runs/train/measure_trained.jsonl")
    if out.exists():
        raise SystemExit(f"{out} already exists. Refusing to append.")
    out.parent.mkdir(parents=True, exist_ok=True)
    service = FiretitanServiceClient(
        api_key=key,
        base_url="https://api.fireworks.ai/training/v1/serverless",
    )
    trainer = service.create_lora_training_client(
        base_model="accounts/fireworks/models/qwen3p8-27b", rank=8
    )
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")
    snapshot = trainer.save_weights_for_sampler("train-r20").result().path
    sampler = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    ids = stable_ids(8, 20)
    probes = {ids[-1]: 0.0, ids[-2]: 0.3}
    print("train probes", probes, flush=True)
    env = ScriptedPGG(ids=ids, seed=20)
    steps = 0
    for t in range(20):
        actions = {}
        last = env.history[-1]["c"] if env.history else {i: 0.0 for i in ids}
        for seat, value in probes.items():
            others = [i for i in ids if i != seat]
            actions[seat] = {
                "message": "",
                "nominate": sorted(others, key=lambda i: last[i], reverse=True)[:2],
                "contribute": value,
            }
        groups = {}
        for seat in ids:
            if seat in probes:
                continue
            text = rendered_prompt(tokenizer, seat, env, order_for(ids, seat, 20, t), [])
            prompt_ids = tokenizer.encode(text)
            sampled = sampler.sample(
                prompt=ModelInput.from_ints(prompt_ids),
                num_samples=4,
                sampling_params={"max_tokens": 80, "temperature": 0.4},
            ).result()
            parsed = []
            for sequence in sampled.sequences:
                decoded = tokenizer.decode(list(sequence.tokens))
                action, ok = repair(parse_model_text(decoded), ids)
                parsed.append((sequence, action, ok))
            actions[seat] = parsed[0][1]
            groups[seat] = (prompt_ids, parsed)
        datums = []
        for seat, (prompt_ids, parsed) in groups.items():
            values = [hold_return(env, {**actions, seat: action}, seat, 20 - t) for _, action, _ in parsed]
            mean = sum(values) / len(values)
            advantages = [value - mean for value in values]
            if len(set(round(a, 6) for a in advantages)) > 1:
                datums.extend(datum_for(prompt_ids, sequence, adv) for (sequence, _, _), adv in zip(parsed, advantages))
                steps += 1
        if datums:
            trainer.forward_backward(datums, "importance_sampling").result()
            trainer.optim_step(
                tinker.AdamParams(learning_rate=2.5e-5, beta1=0.9, beta2=0.95, eps=1e-8, weight_decay=0.0)
            ).result()
            sampler.close()
            snapshot = trainer.save_weights_for_sampler(f"tr{t:02d}").result().path
            sampler = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
        contrib = {i: actions[i]["contribute"] for i in ids}
        noms = {i: actions[i]["nominate"] for i in ids}
        env.record(contrib, noms)
        env.working = env.form_groups(noms)
        env.last_c = contrib
        print("train t", t, "steps", steps, flush=True)
    Path("runs/train/adapter_r20.txt").write_text(snapshot + "\n")
    print("saved", snapshot, "steps", steps, flush=True)
    measure(sampler, tokenizer, out)
    print("wrote", out, flush=True)
    sampler.close()


if __name__ == "__main__":
    main()
