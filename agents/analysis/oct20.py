"""Reproduce the 20 Oct numbers from the files. No pooled p-values.

Usage: python -m agents.analysis.oct20
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


def rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def latency(chunk, reformer, model):
    streak = 0
    for row in chunk:
        if row["t"] < 8:
            continue
        named = sum(reformer in row["action"][seat]["nominate"] for seat in model)
        streak = streak + 1 if named >= 2 else 0
        if streak >= 2:
            return row["t"] - 8
    return "not readmitted"


def episode_table(path: Path) -> list[dict]:
    chunk = rows(path)
    if not chunk:
        return []
    first = chunk[0]
    reformer, steady, zero = first["reformer"], first["steady"], first["zero"]
    model = [i for i in first["ids"] if i not in (reformer, steady, zero)]
    after = [row for row in chunk if row["t"] >= 8]
    possible = len(after) * len(model)

    def named(sid):
        return sum(sid in row["action"][seat]["nominate"] for row in after for seat in model)

    gaps = []
    for row in chunk:
        s = sum(steady in row["action"][seat]["nominate"] for seat in model)
        r = sum(reformer in row["action"][seat]["nominate"] for seat in model)
        gaps.append({"t": row["t"], "gap": s - r, "arm": first["arm"], "seed": first["seed"]})
    contrib = [
        row["action"][seat]["contribute"]
        for row in chunk
        for seat in model
    ]
    fails = defaultdict(int)
    for row in chunk:
        for seat in model:
            fails[row["repair"].get(seat, "ok" if row["ok"][seat] else "non-JSON")] += 1
    return [{
        "arm": first["arm"],
        "seed": first["seed"],
        "memory": first["memory"],
        "reformer_named": named(reformer),
        "steady_named": named(steady),
        "zero_named": named(zero),
        "possible": possible,
        "latency": latency(chunk, reformer, model),
        "mean_contrib": round(sum(contrib) / len(contrib), 3) if contrib else None,
        "names_per_reply": round(
            sum(len(row["action"][seat]["nominate"]) for row in chunk for seat in model) / (len(chunk) * len(model)),
            2,
        ),
        "repair": dict(fails),
        "gaps": gaps,
    }]


def probes_summary() -> list[dict]:
    out = []
    folder = Path("runs/oct20/probes")
    if not folder.exists():
        return out
    for path in folder.glob("*.jsonl"):
        chunk = rows(path)
        by = defaultdict(list)
        for row in chunk:
            by[row["cell"]].append(row)
        for cell, items in by.items():
            n = len(items)
            def rate(key):
                if key not in items[0].get("targets", {}):
                    return None
                sid = items[0]["targets"][key]
                return round(sum(sid in row["partners"] for row in items) / n, 3)
            out.append({
                "model": items[0]["model"],
                "cell": cell,
                "n": n,
                "p_x": rate("x"),
                "p_y": rate("y"),
                "p_target": rate("target"),
                "p_d": rate("d"),
                "repair_failures": sum(1 for row in items if row["repair"] != "ok"),
            })
    return out


def main() -> None:
    episodes = []
    for path in sorted(Path("runs/oct20/game").glob("*.jsonl")) if Path("runs/oct20/game").exists() else []:
        episodes.extend(episode_table(path))
    out = Path("runs/oct20/analysis")
    out.mkdir(parents=True, exist_ok=True)
    with (out / "episodes.csv").open("w", newline="") as handle:
        fields = ["arm", "seed", "memory", "reformer_named", "steady_named", "zero_named", "possible", "latency", "mean_contrib", "names_per_reply", "repair"]
        writer = csv.DictWriter(handle, fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(episodes)
    with (out / "gaps.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, ["arm", "seed", "t", "gap"])
        writer.writeheader()
        for item in episodes:
            writer.writerows(item["gaps"])
    with (out / "probes.csv").open("w", newline="") as handle:
        fields = ["model", "cell", "n", "p_x", "p_y", "p_target", "p_d", "repair_failures"]
        writer = csv.DictWriter(handle, fields)
        writer.writeheader()
        writer.writerows(probes_summary())
    print("wrote", out, "episodes", len(episodes), flush=True)
    print("T1 regression is not fitted here. Two seeds are a preview. Fit named ~ last + earlier in the report from episodes.csv if a library is available.", flush=True)


if __name__ == "__main__":
    main()
