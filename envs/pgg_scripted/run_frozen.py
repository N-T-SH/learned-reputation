"""T2-a smoke: text -> parse -> repair -> env. Speaker is FakeLM until a real provider is chosen."""

from __future__ import annotations

import json
from pathlib import Path

from agents.frozen.fake_lm import complete
from envs.pgg_scripted.env import ScriptedPGG
from envs.pgg_scripted.schema import repair


def parse_model_text(text: str):
    """Turn model text into the object repair() expects.

    A real model returns a string, not a dict. If the string is not usable JSON,
    return the string itself so repair fails closed (empty action, ok False).
    Do not invent a nomination here.
    """
    raise NotImplementedError("T2-a crux: fill parse_model_text")


def prompt_for(seat: int, visible: dict, inbox: list[str]) -> str:
    lines = [
        f"You are seat {seat}.",
        "You may send a short message, nominate partner ids, and set contribution between 0 and 1.",
        "Reply with a JSON object with keys message, nominate, contribute.",
        "You see only your last working set.",
        "Last visible contributions:",
    ]
    for j, c in visible.items():
        lines.append(f"  seat {j}: c={c}")
    lines.append("Messages from the previous round:")
    lines.extend(f"  {m}" for m in inbox) if inbox else lines.append("  (none)")
    return "\n".join(lines)


def run(rounds: int = 5, seed: int = 0) -> Path:
    env = ScriptedPGG(n=4, seed=seed)
    path = Path("runs/pgg/frozen_smoke_seed0.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("")
    inbox = {i: [] for i in env.ids}

    for t in range(rounds):
        texts = {}
        actions = {}
        oks = {}
        for i in env.ids:
            text = complete(i, prompt_for(i, env.visible_c(i), inbox[i]))
            raw = parse_model_text(text)
            action, ok = repair(raw, env.n)
            texts[i] = text
            actions[i] = action
            oks[i] = ok
        contrib = {i: actions[i]["contribute"] for i in env.ids}
        pay = env.payoffs(contrib, env.working)
        noms = {i: set(actions[i]["nominate"]) for i in env.ids}
        row = {
            "t": t,
            "speaker": "FakeLM",
            "working": sorted(env.working),
            "ok": {str(i): oks[i] for i in env.ids},
            "action": {str(i): actions[i] for i in env.ids},
            "pay": {str(i): pay[i] for i in env.ids},
            "text_head": {str(i): texts[i][:80] for i in env.ids},
        }
        with path.open("a") as f:
            f.write(json.dumps(row) + "\n")
        nxt = env.form_groups(noms) or {env.rng.choice(env.ids)}
        env.last_c = contrib
        env.working = nxt
        inbox = {i: [] for i in env.ids}
        for sender, action in actions.items():
            if action["message"]:
                for dest in action["nominate"]:
                    if dest != sender:
                        inbox[dest].append(action["message"])
    print("wrote", path, "speaker=FakeLM")
    return path


if __name__ == "__main__":
    run()
