# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** Log probabilities work in-session. A fresh process cannot reload a snapshot. One 20-round payoff group and one placebo group are measured. Do not open T3.

## Log

| Block | Result |
|---|---|
| Reload | `reload_failed` 404 on `adapter_r20.txt`. Measurement has to finish in the saving process. |
| Payoff 20 | `runs/train/long_payoff.jsonl`. Same ids as placebo. Zero named 1/100. 0.3 named 1/100. High named 73/100. Names per reply 1.76. Repair failures 18. Mean contribution 0.55. |
| Placebo 20 | `runs/train/long_placebo.jsonl`. Zero named 3/100. 0.3 named 11/100. High named 43/100. Names per reply 1.05. Repair failures 41. Mean contribution 0.31. |

## Next

The payoff file names the high seat more than the placebo file. Forty-one placebo replies failed repair, so the gap is not a clean selectivity result. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-06 ~08:38 EDT — payoff versus placebo logged. Parse gap remains.
