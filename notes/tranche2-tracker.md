# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** Frozen and trained 20-round files exist on the same prompt. One episode each. Do not open T3.

## Locks (do not reopen)

1. Comparison is by role, not by id string.
2. Fireworks chat prompt, thinking off. Ledger block is the user message.
3. A training reward is return from that round to the end of the episode.
4. Ids are written on the row. Do not redraw them on resume.

## Log

| Block | Result |
|-------|--------|
| Trained episode | `runs/train/grpo_pilot_chat_r20_seed0.jsonl`. Zero named 25/120. 0.3 named 9/120. Model named model 280/600. Late rounds named neither probe. Updated inside the episode. |
| Frozen episode | `runs/train/fireworks_frozen_r20_seed1.jsonl`. Own ids. Probes fixed: `9glshv` 0, `oo3sb0` 0.3. 20 rounds, 1 repair failure. Zero named 29/120. 0.3 named 24/120. Model named model 329/600. Mean contribution 0.88. Late rounds named zero 5/30 and 0.3 4/30, and named another model seat 125/150. No optimizer step. |

## Next

One episode a side is not a result. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-05 ~05:05 EDT — frozen 20-round before picture logged.
