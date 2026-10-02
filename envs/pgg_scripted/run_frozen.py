"""Frozen smoke: prompt -> speaker text -> parse -> repair -> env step.

SPEAKER=fake uses the stand-in. SPEAKER=openrouter calls OpenRouter.
The log records which one ran. A missing key does not fall back silently.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from agents.frozen.fake_lm import complete as fake_complete
from agents.frozen.openrouter_lm import complete as openrouter_complete
from envs.pgg_scripted.env import ScriptedPGG
from envs.pgg_scripted.schema import repair


def parse_model_text(text: str):
    """Text in, object out. Bad JSON is returned as text so repair fails closed."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


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


def speaker():
    name = os.environ.get("SPEAKER", "fake").strip().lower()
    if name == "fake":
        return "FakeLM", fake_complete
    if name == "openrouter":
        model = os.environ.get("OPENROUTER_MODEL", "openrouter/free")
        return f"OpenRouter:{model}", openrouter_complete
    raise ValueError(f"unknown SPEAKER={name}")


def run(rounds: int = 5, seed: int = 0) -> Path:
    label, complete = speaker()
    env = ScriptedPGG(n=4, seed=seed)
    path = Path("runs/pgg") / ("frozen_smoke_seed0.jsonl" if label == "FakeLM" else "openrouter_smoke_seed0.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("")
    inbox = {i: [] for i in env.ids}

    for t in range(rounds):
        texts, actions, oks = {}, {}, {}
        for i in env.ids:
            text = complete(i, prompt_for(i, env.visible_c(i), inbox[i]))
            raw = parse_model_text(text)
            action, ok = repair(raw, env.n)
            texts[i], actions[i], oks[i] = text, action, ok
        contrib = {i: actions[i]["contribute"] for i in env.ids}
        pay = env.payoffs(contrib, env.working)
        noms = {i: set(actions[i]["nominate"]) for i in env.ids}
        row = {
            "t": t,
            "speaker": label,
            "working": sorted(env.working),
            "ok": {str(i): oks[i] for i in env.ids},
            "action": {str(i): actions[i] for i in env.ids},
            "pay": {str(i): pay[i] for i in env.ids},
            "text_head": {str(i): texts[i][:120] for i in env.ids},
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
    print("wrote", path, "speaker=" + label)
    return path


if __name__ == "__main__":
    run()
