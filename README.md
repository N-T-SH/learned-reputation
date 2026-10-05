# learned-reputation

Code for the LLM-group standing design. Reputation is a pattern in nominations, not a score in the prompt.

Owner: [N-T-SH](https://github.com/N-T-SH). This repo is the only code tree.

## Recreate the environment

Use uv. Do not install into the system Python.

Lab checks, including the scripted controls and a frozen run:

```bash
uv venv --python 3.9 .venv
source .venv/bin/activate
uv pip install ag2
```

Fireworks training smoke. This SDK needs Python 3.11.

```bash
uv venv --python 3.11 .venv-train
source .venv-train/bin/activate
uv pip install 'fireworks-ai[training]>=1.2.11,<2'
```

`.venv/`, `.venv-train/`, and `.env` are not committed. Copy the keys into `.env` at the repo root. Source that file once in a new terminal.

## Run

Scripted gate:

```bash
python -m envs.pgg_scripted.run_controls
```

Frozen file. Flags override `.env`. The key stays in `.env`.

```bash
python -m envs.pgg_scripted.run_frozen --speaker openrouter --model qwen/qwen3.8-27b --groups choice --seats 8 --temperature 0.4 --rounds 20 --episodes 5 --free-rider
```

Training smoke, from `.venv-train`:

```bash
python -m agents.train.grpo_smoke
```

## Handoff

GitHub is the handoff between bots. Pull before a run. Commit the jsonl and a line in `notes/tranche2-tracker.md`. Do not edit `notes/2month-plan.md` from the implementation side.

The shared skill for that loop is `skills/lab-coordination/`.

## Current lock

Public ledger of the last five rounds. Six-character seat ids, new each episode. A lone seat gets isolation 0.8. Two scripted probes, contribution 0 and 0.3, when `--free-rider` is set. Before picture: `runs/pgg/frozen_qwen_qwen3.8-27b_choice_s8_t0.4_ledger_id6_probe_seed0_n5.jsonl`.
