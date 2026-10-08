> **Archived 8 Oct 2026** — see `notes/README.md`. Body below unchanged except link fixes.

# Seed 40 frozen addendum — 7 Oct 2026

Same ids as `runs/train/long_payoff.jsonl`. No step. Console line, file not yet on the remote when this note was written.

| Arm | High named | Zero named | Names per reply | Repair failures |
|---|---|---|---|---|
| Frozen, seed 40 | 69/100 | 2/100 | 1.56 | 17 |
| Payoff | 73/100 | 1/100 | 1.76 | 18 |
| Placebo | 43/100 | 3/100 | 1.05 | 41 |

The payoff step did not move the prior. The placebo step is worse, and it failed repair more often. Do not spend the remaining cap on another training group. Push `runs/train/long_frozen_seed40.jsonl` so the file sits with the other two.
