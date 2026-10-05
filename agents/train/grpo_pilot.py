"""Continue the chat-prompt pilot to 15 rounds.

Replays runs/train/grpo_pilot_chat_seed0.jsonl and appends the missing rounds.
The adapter is a new session. It does not carry the first five steps.
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


def probes_for(ids: list[str]) -> dict[str, float]:
    return {ids[-1]: 0.0, ids[-2]: 0.3}


def scripted(env: ScriptedPGG, probes: dict[str, float]) -> dict:
    last = env.history[-1]["c"] if env.history else {i: 0.0 for i in env.ids}
    actions = {}
    for sid, value in probes.items():
        others = [i for i in env.ids if i != sid]
        actions[sid] = {
            "message": "",
            "nominate": sorted(others, key=lambda i: last[i], reverse=True)[:2],
            "contribute": value,
        }
    return actions


def replay(env: ScriptedPGG, rows: list[dict]) -> None:
    for row in rows:
        actions = row["action"]
        contrib = {i: actions[i]["contribute"] for i in env.ids}
        noms = {i: actions[i]["nominate"] for i in env.ids}
        env.record(contrib, noms)
        env.working = env.form_groups(noms)
        env.last_c = contrib


def hold_return(env: ScriptedPGG, actions: dict, seat: str, rounds_left: int) -> float:
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

    rounds, group = 15, 4
    path = Path("runs/train/grpo_pilot_chat_seed0.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    done = [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []
    service = FiretitanServiceClient(
        api_key=key,
        base_url="https://api.fireworks.ai/training/v1/serverless",
    )
    trainer = service.create_lora_training_client(
        base_model="accounts/fireworks/models/qwen3p8-27b", rank=8
    )
    snapshot = trainer.save_weights_for_sampler("pilot-0004").result().path
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")
    sampler = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    ids = episode_ids(8, 0)
    probes = probes_for(ids)
    env = ScriptedPGG(ids=ids, seed=0)
    replay(env, done)
    print("resume_at", len(done), "adapter", "new session", flush=True)
    steps = 0
    for t in range(len(done), rounds):
        actions = scripted(env, probes)
        groups = {}
        for seat in ids:
            if seat in probes:
                continue
            text = rendered_prompt(tokenizer, seat, env, order_for(ids, seat, 0, t), [])
            prompt_ids = tokenizer.encode(text)
            sampled = sampler.sample(
                prompt=ModelInput.from_ints(prompt_ids),
                num_samples=group,
                sampling_params={"max_tokens": 80, "temperature": 0.4},
            ).result()
            parsed = []
            for sequence in sampled.sequences:
                decoded = tokenizer.decode(list(sequence.tokens))
                action, ok = repair(parse_model_text(decoded), ids)
                parsed.append((sequence, action, ok))
            actions[seat] = parsed[0][1]
            groups[seat] = (prompt_ids, parsed)
        returns = {
            seat: [
                hold_return(env, {**actions, seat: action}, seat, rounds - t)
                for _, action, _ in parsed
            ]
            for seat, (prompt_ids, parsed) in groups.items()
        }
        datums = []
        for seat, (prompt_ids, parsed) in groups.items():
            values = returns[seat]
            mean = sum(values) / len(values)
            advantages = [value - mean for value in values]
            spread = len(set(round(a, 6) for a in advantages)) > 1
            if spread:
                datums.extend(
                    datum_for(prompt_ids, sequence, adv)
                    for (sequence, _, _), adv in zip(parsed, advantages)
                )
                steps += 1
            print("t", t, "seat", seat, "returns", [round(v, 3) for v in values], "step", spread, flush=True)
        if datums:
            trainer.forward_backward(datums, "importance_sampling").result()
            trainer.optim_step(
                tinker.AdamParams(learning_rate=2.5e-5, beta1=0.9, beta2=0.95, eps=1e-8, weight_decay=0.0)
            ).result()
        row = {
            "t": t,
            "prompt": "fireworks-chat",
            "probes": probes,
            "working": sorted(env.working),
            "action": actions,
            "returns": {seat: values for seat, values in returns.items()},
        }
        with path.open("a") as handle:
            handle.write(json.dumps(row) + "\n")
        contrib = {i: actions[i]["contribute"] for i in env.ids}
        noms = {i: actions[i]["nominate"] for i in env.ids}
        env.record(contrib, noms)
        env.working = env.form_groups(noms)
        env.last_c = contrib
    print("wrote", path, "groups_with_spread", steps, flush=True)
    sampler.close()


if __name__ == "__main__":
    main()
