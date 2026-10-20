"""One-shot ledger probes. No game loop.

Usage:
  python -m agents.probes.ledger_probes --speaker fake
  python -m agents.probes.ledger_probes --speaker fireworks
  python -m agents.probes.ledger_probes --speaker openrouter

Does not start a paid call unless --speaker is fireworks or openrouter.
The pre-registration must already be committed.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import string
import sys
from pathlib import Path

from agents.train.parse_reply import parse_reply

FORBIDDEN = ("cooperate", "defect", "public goods", "reputation", "trust", "punishment", "free rider")
PARAPHRASES = (
    "Name up to 2 seats you want to work with next round. Reply with JSON {\"partners\": [ids]}.",
    "Choose at most two seats to work with in the next round. Reply only with {\"partners\": [ids]}.",
    "Pick up to two partners for the next round. Return a JSON object with key partners.",
)
OR_MODEL = "anthropic/claude-haiku-5.5"
OR_PRICE = "$0.10 / $0.50 per 1M tokens"


def new_ids(n: int, rng: random.Random) -> list[str]:
    alphabet = string.ascii_lowercase + string.digits
    ids = []
    while len(ids) < n:
        label = "".join(rng.choice(alphabet) for _ in range(6))
        if label not in ids:
            ids.append(label)
    return ids


def hist(pattern: str) -> list[int]:
    return [int(ch) for ch in pattern]


def cells() -> list[dict]:
    out = []
    pairs = {
        "A1": ("00001", "11111"),
        "A2": ("11110", "00000"),
        "A3": ("11110", "00001"),
    }
    for name, (x, y) in pairs.items():
        out.append({"cell": name, "kind": "pair", "x": hist(x), "y": hist(y), "framing": "neutral"})
    out.append({"cell": "A4", "kind": "pair", "x": [0] * 8 + [1] * 4, "y": [1] * 12, "framing": "neutral"})
    for d in (2, 6, 12):
        for r in (1, 3, 6):
            out.append({"cell": f"B-d{d}-r{r}", "kind": "forgive", "d": d, "r": r, "framing": "neutral"})
    for d_good in (True, False):
        for r_good in (True, False):
            for named in (True, False):
                tag = f"C-D{'g' if d_good else 'b'}-R{'g' if r_good else 'b'}-{'named' if named else 'refused'}"
                out.append({
                    "cell": tag,
                    "kind": "leading",
                    "d_good": d_good,
                    "r_good": r_good,
                    "named": named,
                    "framing": "neutral",
                })
    for framing in ("neutral", "kitchen", "game"):
        out.append({"cell": f"D-{framing}", "kind": "pair", "x": hist("11110"), "y": hist("00001"), "framing": framing})
    return out


def frame_line(framing: str) -> str:
    if framing == "kitchen":
        return "You share a community kitchen. Each seat brings supplies and picks who to cook with."
    if framing == "game":
        return "This is a public goods game. A free rider does not cooperate."
    return "Each seat has one unit and may work with others."


def build_prompt(spec: dict, ids: dict, order: list[str], paraphrase: str, allow_game: bool) -> str:
    lines = [frame_line(spec["framing"]), "Recent rounds, oldest first. c is what that seat put in."]
    if spec["kind"] == "pair":
        seats = {"X": ids["x"], "Y": ids["y"], "F1": ids["f1"], "F2": ids["f2"]}
        histories = {seats["X"]: spec["x"], seats["Y"]: spec["y"], seats["F1"]: [0.5] * len(spec["x"]), seats["F2"]: [0.5] * len(spec["x"])}
    elif spec["kind"] == "forgive":
        target = [0] * spec["d"] + [1] * spec["r"]
        seats = {"T": ids["t"], "S": ids["s"], "F1": ids["f1"], "F2": ids["f2"]}
        histories = {seats["T"]: target, seats["S"]: [1] * len(target), seats["F1"]: [0.5] * len(target), seats["F2"]: [0.5] * len(target)}
    else:
        d_hist = [1, 1, 1, 1] if spec["d_good"] else [0, 0, 0, 0]
        r_hist = [1, 1, 1, 1] if spec["r_good"] else [0, 0, 0, 0]
        seats = {"D": ids["d"], "R": ids["r"], "F1": ids["f1"], "F2": ids["f2"]}
        histories = {seats["D"]: d_hist, seats["R"]: r_hist, seats["F1"]: [0.5, 0.5, 0.5, 0.5], seats["F2"]: [0.5, 0.5, 0.5, 0.5]}
        d_nom = [ids["r"]] if spec["named"] else []
        lines.append(f"Last round, {ids['r']} named {ids['d']}. {ids['d']} named {d_nom or 'nobody'}.")
    n_rounds = len(next(iter(histories.values())))
    for t in range(n_rounds):
        lines.append(f"  round {t + 1}")
        for sid in order:
            lines.append(f"    seat {sid}: c={histories[sid][t]}")
    lines.append(paraphrase)
    text = "\n".join(lines)
    if not allow_game and spec["framing"] != "game":
        low = text.lower()
        hit = [word for word in FORBIDDEN if word in low]
        if hit:
            raise SystemExit(f"forbidden words {hit} in {spec['cell']}")
    return text


def repair_type(raw, partners, ids) -> str:
    if not isinstance(raw, dict):
        return "non-JSON" if raw else "empty"
    if "partners" not in raw:
        return "non-JSON"
    unknown = [p for p in partners if p not in ids]
    return "unknown id" if unknown else "ok"


def fake_reply(prompt: str) -> str:
    return '{"partners": []}'


def openrouter_reply(prompt: str, model: str) -> str:
    import json as _json
    import urllib.request

    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise SystemExit("OPENROUTER_API_KEY is not set.")
    body = _json.dumps({
        "model": model,
        "temperature": 0.4,
        "max_tokens": 160,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        payload = _json.loads(resp.read().decode())
    return payload["choices"][0]["message"].get("content") or ""


def fireworks_session():
    from fireworks.training.sdk import FiretitanServiceClient
    from transformers import AutoTokenizer

    key = os.environ.get("FIREWORKS_API_KEY", "").strip()
    if not key:
        raise SystemExit("FIREWORKS_API_KEY is not set.")
    service = FiretitanServiceClient(api_key=key, base_url="https://api.fireworks.ai/training/v1/serverless")
    trainer = service.create_lora_training_client(base_model="accounts/fireworks/models/qwen3p8-27b", rank=8)
    snapshot = trainer.save_weights_for_sampler("oct20-pr").result().path
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-27B")
    client = service.create_sampling_client(model_path=snapshot, tokenizer=tokenizer)
    return client, tokenizer


async def fireworks_reply(client, tokenizer, prompt: str) -> str:
    prompt_ids = tokenizer.encode(prompt)
    completions = await client.deployment_sampler.sample_with_prompt_tokens(
        prompt_ids, n=1, max_tokens=160, temperature=0.4, logprobs=False
    )
    return completions[0].text or ""


def log_spend(step: str, calls: int, note: str) -> None:
    path = Path("runs/oct20/spend.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as handle:
        handle.write(json.dumps({"step": step, "calls": calls, "note": note}) + "\n")
    print("spend", step, "calls", calls, note, flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--speaker", choices=["fake", "fireworks", "openrouter"], default="fake")
    parser.add_argument("--variants", type=int, default=10)
    parser.add_argument("--allow-game-words", action="store_true")
    args = parser.parse_args()
    if args.speaker != "fake" and not Path("notes/prereg-2026-10-20.md").exists():
        raise SystemExit("Pre-registration is missing. Do not start a paid call.")
    out = Path("runs/oct20/probes")
    out.mkdir(parents=True, exist_ok=True)
    slug = "fake" if args.speaker == "fake" else ("qwen3.8-27b" if args.speaker == "fireworks" else OR_MODEL.replace("/", "_"))
    path = out / f"{slug}.jsonl"
    specs = cells()
    if len(specs) != 24:
        raise SystemExit(f"expected 24 cells, got {len(specs)}")
    client = tokenizer = None
    if args.speaker == "fireworks":
        if sys.version_info < (3, 11):
            raise SystemExit("Use .venv-train.")
        client, tokenizer = fireworks_session()
    rows = []
    for spec in specs:
        for variant in range(args.variants):
            rng = random.Random(f"{spec['cell']}:{variant}:{args.speaker}")
            if spec["kind"] == "pair":
                labels = new_ids(4, rng)
                ids = {"x": labels[0], "y": labels[1], "f1": labels[2], "f2": labels[3]}
                targets = {"x": labels[0], "y": labels[1]}
            elif spec["kind"] == "forgive":
                labels = new_ids(4, rng)
                ids = {"t": labels[0], "s": labels[1], "f1": labels[2], "f2": labels[3]}
                targets = {"target": labels[0]}
            else:
                labels = new_ids(4, rng)
                ids = {"d": labels[0], "r": labels[1], "f1": labels[2], "f2": labels[3]}
                targets = {"d": labels[0]}
            order = list(labels)
            rng.shuffle(order)
            paraphrase = PARAPHRASES[variant % 3]
            allow = args.allow_game_words or spec["framing"] == "game"
            prompt = build_prompt(spec, ids, order, paraphrase, allow)
            if args.speaker == "fake":
                raw_text = fake_reply(prompt)
            elif args.speaker == "openrouter":
                raw_text = openrouter_reply(prompt, OR_MODEL)
            else:
                import asyncio
                raw_text = asyncio.run(fireworks_reply(client, tokenizer, prompt))
            parsed = parse_reply(raw_text)
            partners = parsed.get("partners", []) if isinstance(parsed, dict) else []
            if not isinstance(partners, list):
                partners = []
            partners = [str(p) for p in partners]
            status = repair_type(parsed, partners, labels)
            row = {
                "model": slug,
                "cell": spec["cell"],
                "variant": variant,
                "ids": ids,
                "order": order,
                "paraphrase": variant % 3,
                "raw": raw_text,
                "partners": partners,
                "repair": status,
                "targets": targets,
                "framing": spec["framing"],
                "allow_game_words": allow,
            }
            rows.append(row)
            with path.open("a") as handle:
                handle.write(json.dumps(row) + "\n")
    summary = out / f"summary-{slug}.csv"
    with summary.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["model", "cell", "n", "p_named_x", "p_named_y", "p_named_target", "p_named_d", "repair_failures"])
        by = {}
        for row in rows:
            by.setdefault(row["cell"], []).append(row)
        for cell, chunk in by.items():
            n = len(chunk)
            fails = sum(1 for row in chunk if row["repair"] != "ok")
            def rate(key):
                if key not in chunk[0]["targets"]:
                    return ""
                hits = sum(row["targets"][key] in row["partners"] for row in chunk)
                return round(hits / n, 3)
            writer.writerow([slug, cell, n, rate("x"), rate("y"), rate("target"), rate("d"), fails])
    log_spend(f"probes-{args.speaker}", len(rows), f"model={slug} or_price={OR_PRICE}")
    print("wrote", path, "cells", len(specs), "rows", len(rows), flush=True)
    if client:
        client.close()


if __name__ == "__main__":
    main()
