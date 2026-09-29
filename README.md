# learned-reputation

Code for the LLM-group standing design (mechanisms, not hardcoded reputation scores).

Owner: [N-T-SH](https://github.com/N-T-SH). This repo is the **only** code tree going forward. `resilient-lab` keeps older experiments.

## Status

- Week 0 concepts: done (Ueshima / RepuNet withhold / PGG / GRPO).
- Week 1: scripted linear PGG + local visibility + ± include rules.
- No LLM seats until a regression recovers the scripted positive rule and is ~0 on the null.

## Layout

```
envs/pgg_scripted/   # 4-seat toy, no LLM
  env.py             # payoffs + local visible_c
  policies.py        # CRUX: include_next (not implemented)
  run_controls.py    # writes runs/pgg/{positive,null}_seed0.jsonl
notes/               # locked specs only
runs/pgg/
```

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m envs.pgg_scripted.run_controls
```

Will raise until you fill `include_next` in `policies.py`.

## Locked controls

- Positive: include j next round iff last visible c_j ≥ 0.5 (None → include).
- Null: each round, include self + each other seat with p=0.5; ignore history.
- Visibility: local (last working-set contributions).
- PGG toy: n=4, r=1.6, y=1, isolation=0.8.
