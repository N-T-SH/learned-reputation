"""Frozen run. The seat id in the prompt is the seat id in the log.

Each episode draws fresh 6-character ids. Each seat sees the ledger in its own order.
--free-rider adds two scripted seats: contribution 0 and contribution 0.3.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import string
import time
from datetime import datetime, timezone
from pathlib import Path

from agents.frozen.fake_lm import complete as fake_complete
from agents.frozen.openrouter_lm import complete as openrouter_complete
from envs.pgg_scripted.env import ScriptedPGG
from envs.pgg_scripted.schema import repair

ALPHABET = string.ascii_lowercase + string.digits


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


def episode_ids(n: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    ids = set()
    while len(ids) < n:
        ids.add("".join(rng.choice(ALPHABET) for _ in range(6)))
    ids = list(ids)
    rng.shuffle(ids)
    return ids


def order_for(ids: list[str], seat: str, episode: int, t: int) -> list[str]:
    order = list(ids)
    random.Random(f"{episode}:{t}:{seat}").shuffle(order)
    return order


def prompt_for(seat: str, env: ScriptedPGG, order: list[str], inbox: list[str]) -> str:
    lines = [
        f"You are seat {seat}.",
        "You may send a short message, nominate partner ids, and set contribution between 0 and 1.",
        "Reply with a JSON object with keys message, nominate, contribute.",
        "Recent rounds, newest last. c is contribution. nom is who that seat named.",
    ]
    if not env.history:
        lines.append("  (no prior round)")
    for round_i, item in enumerate(env.history, start=1):
        lines.append(f"  round {round_i}")
        for sid in order:
            lines.append(f"    seat {sid}: c={item['c'][sid]} nom={item['nom'][sid]}")
    lines.append("Messages from the previous round:")
    lines.extend(f"  {m}" for m in inbox) if inbox else lines.append("  (none)")
    return "\n".join(lines)


def scripted_action(env: ScriptedPGG, seat: str, contribute: float) -> dict:
    last = env.history[-1]["c"] if env.history else {i: 0.0 for i in env.ids}
    others = [i for i in env.ids if i != seat]
    top = sorted(others, key=lambda i: last[i], reverse=True)[:2]
    return {"message": "", "nominate": top, "contribute": contribute}


def speaker(name: str | None, model: str | None, temperature: float):
    chosen = (name or os.environ.get("SPEAKER") or "fake").strip().lower()
    pinned = (model or os.environ.get("OPENROUTER_MODEL") or "openrouter/free").strip()
    if chosen == "fake":
        return "FakeLM", fake_complete
    if chosen == "openrouter":
        def call(seat: str, prompt: str) -> str:
            return openrouter_complete(0, prompt, model=pinned, reasoning_off=True, temperature=temperature)
        return f"OpenRouter:{pinned}", call
    raise ValueError(f"unknown speaker={chosen}")


def load_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def load_seats(path: Path) -> dict[tuple[int, int, str], str]:
    saved = {}
    for row in load_rows(path):
        saved[(int(row["episode"]), int(row["t"]), str(row["seat"]))] = row["text"]
    return saved


def save_seat(path: Path, episode: int, t: int, seat: str, text: str) -> None:
    with path.open("a") as f:
        f.write(json.dumps({"episode": episode, "t": t, "seat": seat, "text": text}) + "\n")
        f.flush()


def replay(env: ScriptedPGG, rows: list[dict]) -> dict:
    inbox = {i: [] for i in env.ids}
    for row in rows:
        actions = row["action"]
        contrib = {i: actions[i]["contribute"] for i in env.ids}
        noms = {i: actions[i]["nominate"] for i in env.ids}
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
    tag = "ledger_id6_probe" if free_rider else "ledger_id6"
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

    for ep in range(episodes):
        have = by_ep.get(ep, [])
        if len(have) >= rounds:
            print("episode", ep, "already done")
            continue
        ids = episode_ids(seats, seed + ep)
        probes = {ids[-1]: 0.0, ids[-2]: 0.3} if free_rider else {}
        env = ScriptedPGG(ids=ids, seed=seed + ep)
        inbox = replay(env, have)
        ep_started = time.time()
        for t in range(len(have), rounds):
            round_started = time.time()
            texts, actions, oks = {}, {}, {}
            for sid in env.ids:
                if sid in probes:
                    actions[sid] = scripted_action(env, sid, probes[sid])
                    texts[sid], oks[sid] = f"scripted c={probes[sid]}", True
                    continue
                key = (ep, t, sid)
                if key in saved:
                    text = saved[key]
                else:
                    text = complete(sid, prompt_for(sid, env, order_for(ids, sid, ep, t), inbox[sid]))
                    save_seat(seats_path, ep, t, sid, text)
                    saved[key] = text
                action, ok = repair(parse_model_text(text), env.ids)
                texts[sid], actions[sid], oks[sid] = text, action, ok
            contrib = {i: actions[i]["contribute"] for i in env.ids}
            pay = env.payoffs(contrib, env.working)
            noms = {i: actions[i]["nominate"] for i in env.ids}
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
                "ids": ids,
                "probes": probes,
                "working": sorted(env.working),
                "ok": {i: oks[i] for i in env.ids},
                "action": actions,
                "pay": pay,
                "text_head": {i: texts[i][:120] for i in env.ids},
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
