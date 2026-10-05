---
name: lab-coordination
description: "Coordinate the learned-reputation lab across bots with uv and GitHub. Use when setting up the environment, running a frozen or training smoke, updating a tracker, or handing work between the implementation bot and the plan bot."
type: workflow
lifecycle: active
---

# Lab coordination — uv and GitHub

Use this when more than one bot works on `N-T-SH/learned-reputation`. GitHub is the handoff. Do not rely on chat memory.

## Environment

Use uv. Do not use system pip. Do not pass `--break-system-packages`.

Lab checks that do not need Fireworks:

```bash
uv venv --python 3.9 .venv
source .venv/bin/activate
uv pip install ag2
```

Fireworks training smoke:

```bash
uv venv --python 3.11 .venv-train
source .venv-train/bin/activate
uv pip install 'fireworks-ai[training]>=1.2.11,<2'
```

Do not commit `.venv/`, `.venv-train/`, or `.env`. A new key means source `.env` once in that terminal. Do not repeat that source in later commands.

## GitHub handoff

Pull before editing or running. Commit gate logs and notes. Do not commit secrets.

| File | Who writes | Who reads |
|---|---|---|
| `notes/tranche2-tracker.md` | implementation bot | plan bot |
| `notes/for-plan-bot.md` | implementation bot | plan bot |
| `notes/for-implementation-bot.md` | plan bot | implementation bot |
| `notes/t2-gate.md` | implementation bot, from a real log | both |
| `runs/pgg/*.jsonl` | the run, then commit | both |

Do not edit `notes/2month-plan.md` from the implementation side. The plan bot syncs it.

Write plain sentences in notes. A result is a file path plus what the log showed. Do not claim emergence from a frozen file.

## A run

1. `git pull --ff-only`
2. Run from the matching venv.
3. Push the jsonl and a tracker line in the same session.
4. If the process was already running, do not pull in that terminal.

## Common failures

| Error | Do |
|---|---|
| externally-managed-environment | Install into `.venv` or `.venv-train` with uv, not system Python |
| OPENROUTER_API_KEY is not set | Source `.env` once |
| FIREWORKS_API_KEY is not set | Add the key, source once, stay in `.venv-train` |
| Python older than 3.11 on the training smoke | Activate `.venv-train` |
