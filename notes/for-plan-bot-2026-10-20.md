# For the planning bot, 20 Oct 2026

**Repo:** `N-T-SH/learned-reputation`
**Pre-registration:** `878692c` in `notes/prereg-2026-10-20.md`. Committed before any paid call.
**Status:** v1 and v2 game files are in. Report is `notes/report-2026-10-20-v2.md`.

## Spend

`runs/oct20/spend.jsonl` has call counts only, not dollars.

- Fake dry run: 48 calls, $0.
- Fireworks Qwen 3.8 27B probes: 240 calls, $0.24.
- OpenRouter `anthropic/claude-haiku-5.5`: 240 calls, $0.03.
- v1 game runs: 8 episodes, about $1.
- v2 game runs: 4 episodes, about $0.50.

Cap is $8. Nitesh has the exact total. Rough running total is about $1.80.

## What can be scored

`runs/oct20/probes/summary.csv` is wrong. It scored every variant against the first variant's ids. The rates below are recomputed from each row's own `targets`. Use the jsonl, not that csv.

### Qwen 3.8 27B, Fireworks, thinking off, temperature 0.4

File: `runs/oct20/probes/qwen3.8-27b.jsonl`. 240 calls. Repair: 192 ok, 33 non-JSON, 15 empty.

| Cell | Contrast | Rate |
|---|---|---|
| A1 | same last move, opposite record | Y (all 1s) 0.7, X (four 0s then 1) 0.3 |
| A2 | good record then a 0, vs all 0s | both 0.1 |
| A3 | record and last move conflict | X (good record, bad last) 0.1, Y (bad record, good last) 0.3 |
| A4 | 12-round reformer vs steady | reformer 0.3, steady 0.7 |
| D-neutral | A3 wording | X 0.3, Y 0.2 |
| D-kitchen | kitchen wording | 9 of 10 failed to parse |
| D-game | explicit game words | both 0.0, 5 of 10 failed |

T4, as written, failed on this model. P(named | good record, bad last move) is 0.1. P(named | bad record, good last move) is 0.3. The last move beat the longer record on the conflict cell.

### Haiku 5.5, OpenRouter

File: `runs/oct20/probes/anthropic_claude-haiku-5.5.jsonl`. 240 calls. Repair: 9 ok, 5 unknown id, 9 non-JSON, 217 empty. Not a behavioral result. Left out of the scored report.

## v2, rules in the prompt

Four episodes. Repair 0 of 480. Same seed now shares id order and role seats.

- Window seed 0: reformer 4/80, steady 16, zero 24, not readmitted, contribution 0.721, partners per reply 0.98.
- Window seed 1: reformer 0/80, steady 0, zero 16, not readmitted, contribution 0.508, partners per reply 0.98.
- Full seed 0: reformer 16/80, steady 0, zero 32, not readmitted, contribution 0.700, partners per reply 0.97.
- Full seed 1: reformer 32/80, steady 0, zero 42, latency 1, contribution 0.613, partners per reply 1.32.

P1 failed. P3 failed. P4 failed. T1 failed. T2 reported. T3 not tested. Full report: `notes/report-2026-10-20-v2.md`.
