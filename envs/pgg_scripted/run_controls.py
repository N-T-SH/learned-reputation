"""Run scripted ± controls, write JSONL. Fill include_next first."""

from __future__ import annotations

import json
from pathlib import Path

from envs.pgg_scripted.env import ScriptedPGG
from envs.pgg_scripted.policies import include_next


def run(mode: str, rounds: int = 30, seed: int = 0, out: str = ""):
    env = ScriptedPGG(seed=seed)
    rng = env.rng
    path = Path(out or f"runs/pgg/{mode}_seed{seed}.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("")

    for t in range(rounds):
        contrib = {i: 1.0 if rng.random() > 0.4 else 0.0 for i in env.ids}
        pay = env.payoffs(contrib, env.working)
        noms = {i: include_next(i, env.visible_c(i), mode, rng) for i in env.ids}
        rec = {
            "t": t,
            "mode": mode,
            "working": sorted(env.working),
            "contrib": {str(k): v for k, v in contrib.items()},
            "pay": {str(k): v for k, v in pay.items()},
            "noms": {str(k): sorted(v) for k, v in noms.items()},
        }
        with path.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        nxt = env.form_groups(noms)
        if not nxt:
            nxt = {rng.choice(env.ids)}
        env.last_c = contrib
        env.working = nxt

    print("wrote", path, "last working", sorted(env.working))


if __name__ == "__main__":
    run("positive")
    run("null")
