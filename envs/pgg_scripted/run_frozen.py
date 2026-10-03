"""Frozen run. Prompt shows a public ledger. Labels are shuffled per episode.

Logs keep real seat ids. A lone or empty working set is isolation, not a pot.
A paid reply is saved before the next seat is called.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from agents.frozen.fake_lm import complete as fake_complete
from agents.frozen.openrouter_lm import complete as openrouter_complete
from envs.pgg_scripted.env import ScriptedPGG
from envs.pgg_scripted.schema import repair


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_model_text(text: str):
    raw = text.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?", "", raw).strip()
        raw = re.sub(r"```$", "", raw).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start, end = raw.find("{"), raw.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(raw[start : end + 1])
            except json.JSONDecodeError:
                return text
        return text


def labels_for(n: int, seed: int) -> tuple[dict[int, int], dict[int, int]]:
    order = list(range(n))
    random.Random(seed).shuffle(order)
    real_to_show = {real: show for show, real in enumerate(order)}
    show_to_real = {show: real for real, show in real_to_show.items()}
    return real_to_show, show_to_real


def prompt_for(show_id: int, env: ScriptedPGG, real_to_show: dict[int, int], inbox: list[str]) -> str:
    lines = [
        f"You are seat {show_id}.",
        "You may send a short message, nominate partner ids, and set contribution between 0 and 1.",
        "Reply with a JSON object with keys message, nominate, contribute.",
        "Recent rounds, newest last. c is contribution. nom is who that seat named.",
    ]
    if not env.history:
        lines.append("  (no prior round)")
    for round_i, item in enumerate(env.history, start=1):
        lines.append(f"  round {round_i}")
        for real in sorted(env.ids, key=lambda i: real_to_show[i]):
            show = real_to_show[real]
            named = [real_to_show[j] for j in item["nom"][real]]
            lines.append(f"    seat {show}: c={item['c'][real]} nom={named}")
    lines.append("Messages from the previous round:")
    lines.extend(f"  {m}" for m in inbox) if inbox else lines.append("  (none)")
    return "\n".join(lines)


def to_real(action: dict, show_to_real: dict[int, int]) -> dict:
    return {
        "message": action["message"],
        "nominate": [show_to_real[j] for j in action["nominate"] if j in show_to_real],
        "contribute": action["contribute"],
    }


def free_rider_action(env: ScriptedPGG, seat: int) -> dict:
    last = env.history[-1]["c"] if env.history else {i: 0.0 for i in env.ids}
    others = [i for i in env.ids if i != seat]
    top = sorted(others, key=lambda i: last[i], reverse=True)[:2]
    return {"message": "", "nominate": top, "contribute": 0.0}


def speaker(name: str | None, model: str | None, temperature: float):
    chosen = (name or os.environ.get("SPEAKER") or "fake").strip().lower()
    pinned = (model or os.environ.get("OPENROUTER_MODEL") or "openrouter/free").strip()
    if chosen == "fake":
        return "FakeLM", fake_complete
    if chosen == "openrouter":
        def call(seat: int, prompt: str) -> str:
            return openrouter_complete(
                seat, prompt, model=pinned, reasoning_off=True, temperature=temperature
            )
        return f"OpenRouter:{pinned}", call
    raise ValueError(f"unknown speaker={chosen}")


def load_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def load_seats(path: Path) -> dict[tuple[int, int, int], str]:
    saved = {}
    for row in load_rows(path):
        saved[(int(row["episode"]), int(row["t"]), int(row["seat"]))] = row["text"]
    return saved


def save_seat(path: Path, episode: int, t: int, seat: int, text: str) -> None:
    with path.open("a") as f:
        f.write(json.dumps({"episode": episode, "t": t, "seat": seat, "text": text}) + "\n")
        f.flush()


def replay(env: ScriptedPGG, rows: list[dict]) -> dict:
    inbox = {i: [] for i in env.ids}
    for row in rows:
        actions = {int(k): v for k, v in row["action"].items()}
        contrib = {i: actions[i]["contribute"] for i in env.ids}
        noms = {i: set(actions[i]["nominate"]) for i in env.ids}
        env.record(contrib, noms)
        nxt = set(env.ids) if row.get("groups") == "fixed" else env.form_groups(noms)
        env.last_c = contrib
        env.working = nxt
        inbox = {i: [] for i in env.ids}
        for sender, action in actions.items():
            if action["message"]:
                for dest in action["nominate"]:
                    if dest != sender and dest in inbox:
                        inbox[dest].append(action["message"])
    return inbox


def run(
    rounds: int = 5,
    seed: int = 0,
    speaker_name: str | None = None,
    model: str | None = None,
    groups: str = "choice",
    episodes: int = 1,
    seats: int = 4,
    temperature: float = 0.0,
    free_rider: bool = False,
) -> Path:
    label, complete = speaker(speaker_name, model, temperature)
    slug = "fake" if label == "FakeLM" else label.split(":", 1)[-1].replace("/", "_")
    tag = "ledger" + ("_fr" if free_rider else "")
    path = Path("runs/pgg") / f"frozen_{slug}_{groups}_s{seats}_t{temperature}_{tag}_seed{seed}_n{episodes}.jsonl"
    seats_path = path.with_suffix(".seats.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    done = load_rows(path)
    saved = load_seats(seats_path)
    by_ep: dict[int, list[dict]] = {}
    for row in done:
        by_ep.setdefault(int(row["episode"]), []).append(row)
    run_started = time.time()
    print("started", stamp(), flush=True)
    rider = seats - 1 if free_rider else None

    for ep in range(episodes):
        have = by_ep.get(ep, [])
        if len(have) >= rounds:
            print("episode", ep, "already done")
            continue
        env = ScriptedPGG(n=seats, seed=seed + ep)
        real_to_show, show_to_real = labels_for(seats, seed + ep)
        inbox = replay(env, have)
        ep_started = time.time()
        for t in range(len(have), rounds):
            round_started = time.time()
            texts, actions, oks = {}, {}, {}
            for i in env.ids:
                if i == rider:
                    actions[i] = free_rider_action(env, i)
                    texts[i], oks[i] = "scripted free rider", True
                    continue
                key = (ep, t, i)
                if key in saved:
                    text = saved[key]
                    print("reuse", "episode", ep, "t", t, "seat", i)
                else:
                    text = complete(i, prompt_for(real_to_show[i], env, real_to_show, inbox[i]))
                    save_seat(seats_path, ep, t, i, text)
                    saved[key] = text
                action, ok = repair(parse_model_text(text), env.n)
                texts[i], actions[i], oks[i] = text, to_real(action, show_to_real), ok
            contrib = {i: actions[i]["contribute"] for i in env.ids}
            pay = env.payoffs(contrib, env.working)
            noms = {i: set(actions[i]["nominate"]) for i in env.ids}
            finished = time.time()
            row = {
                "episode": ep,
                "t": t,
                "finished_at": stamp(),
                "round_seconds": round(finished - round_started, 1),
                "elapsed_seconds": round(finished - run_started, 1),
                "speaker": label,
                "reasoning": "off",
                "temperature": temperature,
                "seats": seats,
                "groups": groups,
                "ledger": True,
                "label_map": {str(real): show for real, show in real_to_show.items()},
                "working": sorted(env.working),
                "ok": {str(i): oks[i] for i in env.ids},
                "action": {str(i): actions[i] for i in env.ids},
                "pay": {str(i): pay[i] for i in env.ids},
                "text_head": {str(i): texts[i][:120] for i in env.ids},
            }
            with path.open("a") as f:
                f.write(json.dumps(row) + "\n")
                f.flush()
            env.record(contrib, noms)
            nxt = set(env.ids) if groups == "fixed" else env.form_groups(noms)
            env.last_c = contrib
            env.working = nxt
            inbox = {i: [] for i in env.ids}
            for sender, action in actions.items():
                if action["message"]:
                    for dest in action["nominate"]:
                        if dest != sender and dest in inbox:
                            inbox[dest].append(action["message"])
        print("episode", ep, "done", "seconds", round(time.time() - ep_started, 1), flush=True)
    total = round(time.time() - run_started, 1)
    print(
        "wrote", path, "speaker=" + label, "groups=" + groups,
        "reasoning=off", "temperature=" + str(temperature), "seconds=" + str(total),
    )
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Frozen PGG smoke. Flags override .env.")
    parser.add_argument("--speaker", choices=["fake", "openrouter"])
    parser.add_argument("--model")
    parser.add_argument("--groups", choices=["choice", "fixed"], default="choice")
    parser.add_argument("--rounds", type=int, default=5)
    parser.add_argument("--episodes", type=int, default=1)
    parser.add_argument("--seats", type=int, default=4)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--free-rider", action="store_true")
    args = parser.parse_args()
    run(
        rounds=args.rounds,
        seed=args.seed,
        speaker_name=args.speaker,
        model=args.model,
        groups=args.groups,
        episodes=args.episodes,
        seats=args.seats,
        temperature=args.temperature,
        free_rider=args.free_rider,
    )


if __name__ == "__main__":
    main()
