# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** Fireworks frozen chat file parsed. It is the before picture for the next pilot. Do not compare it with the OpenRouter file. Do not open T3.

## Locks (do not reopen)

1. Visibility: public ledger. Last five rounds. Six-character ids, new each episode.
2. Groups: both must nominate each other. A lone seat gets isolation, 0.8.
3. Units: y=1, r=1.6, isolation 0.8.
4. Fireworks comparison prompt: ledger block as the user message, thinking off. Shared by `agents/train/prompt.py`.
5. No reputation scalar and no game-theory jargon in prompts.
6. All model text enters the env only through `repair`.
7. A training reward is return from that round to the end of the episode.

## Exit criteria

- [x] OpenRouter probe file logged
- [x] Fireworks frozen chat file logged. `runs/train/fireworks_frozen_seed0.jsonl`
- [ ] Pilot on that same prompt, then a comparison with the Fireworks frozen file
- [ ] Tracker marked FINISHED

## Log

| Block | Result |
|-------|--------|
| OpenRouter probe | Zero named 15/570 after round 0. 0.3 named 21/570. Different endpoint. |
| Plain Fireworks pilot | 13 of 30 continuing actions failed repair. Not the comparison. |
| Fireworks frozen chat | 30 of 30 ok. Round 0 nominations empty, so round 1 working set was empty. Later rounds formed groups. Contributions 0.5 to 1.0, mean 0.94. Zero named 9/30. 0.3 named 8/30. Model named model 45/150. No optimizer step. |

## Next

Run `python -m agents.train.grpo_pilot` on this prompt. Compare with this file, not the OpenRouter file. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-05 ~03:41 EDT — Fireworks frozen chat file parsed. T2 not finished.
