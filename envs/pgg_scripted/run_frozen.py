"""Frozen smoke: prompt -> speaker text -> parse -> repair -> env step.

Flags win. Environment is the fallback. The key is only read from the environment.
--groups choice uses nominations. --groups fixed ignores them and keeps every seat in.
"""

from __future__ import annotations

import argparse
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


def speaker(name: str | None = None, model: str | None = None):
    chosen = (name or os.environ.get("SPEAKER") or "fake").strip().lower()
    pinned = (model or os.environ.get("OPENROUTER_MODEL") or "openrouter/free").strip()
    if chosen == "fake":
        return "FakeLM", fake_complete
    if chosen == "openrouter":
        def call(seat: int, prompt: str) -> str:
            return openrouter_complete(seat, prompt, model=pinned)
        return f"OpenRouter:{pinned}", call
    raise ValueError(f"unknown speaker={chosen}")


def run(
    rounds: int = 5,
    seed: int = 0,
    speaker_name: str | None = None,
    model: str | None = None,
    groups: str = "choice",
) -> Path:
    label, complete = speaker(speaker_name, model)
    env = ScriptedPGG(n=4, seed=seed)
    slug = "fake" if label == "FakeLM" else label.split(":", 1)[-1].replace("/", "_")
    path = Path("runs/pgg") / f"frozen_{slug}_{groups}_seed{seed}.jsonl"
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
            "groups": groups,
            "working": sorted(env.working),
            "ok": {str(i): oks[i] for i in env.ids},
            "action": {str(i): actions[i] for i in env.ids},
            "pay": {str(i): pay[i] for i in env.ids},
            "text_head": {str(i): texts[i][:120] for i in env.ids},
        }
        with path.open("a") as f:
            f.write(json.dumps(row) + "\n")
        if groups == "fixed":
            nxt = set(env.ids)
        else:
            nxt = env.form_groups(noms) or {env.rng.choice(env.ids)}
        env.last_c = contrib
        env.working = nxt
        inbox = {i: [] for i in env.ids}
        for sender, action in actions.items():
            if action["message"]:
                for dest in action["nominate"]:
                    if dest != sender:
                        inbox[dest].append(action["message"])
    print("wrote", path, "speaker=" + label, "groups=" + groups)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Frozen PGG smoke. Flags override .env.")
    parser.add_argument("--speaker", choices=["fake", "openrouter"], help="fallback: SPEAKER in .env, else fake")
    parser.add_argument("--model", help="OpenRouter model id. Fallback: OPENROUTER_MODEL, else openrouter/free")
    parser.add_argument("--groups", choices=["choice", "fixed"], default="choice")
    parser.add_argument("--rounds", type=int, default=5)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    run(
        rounds=args.rounds,
        seed=args.seed,
        speaker_name=args.speaker,
        model=args.model,
        groups=args.groups,
    )


if __name__ == "__main__":
    main()
