# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** One 20-round episode finished. Probes stayed fixed. Not a held-out comparison. Do not open T3.

## Locks (do not reopen)

1. Visibility: public ledger. Last five rounds. Ids written on the row, not redrawn.
2. Groups: both must nominate each other. A lone seat gets isolation, 0.8.
3. Units: y=1, r=1.6, isolation 0.8.
4. Fireworks comparison prompt: ledger block as the user message, thinking off.
5. A training reward is return from that round to the end of the episode.
6. Do not resume an episode by drawing ids again.

## Log

| Block | Result |
|-------|--------|
| 15-round file | Probe seats changed at round 5. Do not use. |
| 20-round episode | `runs/train/grpo_pilot_chat_r20_seed0.jsonl`. Probes fixed: `vpuemo` 0, `9afza5` 0.3. 120 groups, 65 with spread, 2 empty continuing actions. Zero named 25/120. 0.3 named 9/120. Model named model 280/600. Mean contribution 0.77. Early (rounds 0–4) named zero 13/30 and 0.3 5/30. Late (rounds 15–19) named neither probe, and named another model seat 118/150. Updates happened inside the episode. |

## Next

A comparison needs a frozen file on these ids and this prompt, then a trained file that was not updated in the measured rounds. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-05 ~04:34 EDT — 20-round episode, probes fixed, not a held-out result.
