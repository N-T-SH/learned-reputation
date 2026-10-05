# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** Return-to-go pilot ran. Nine of thirty groups took a step. Not a learning result. Do not open T3.

## Locks (do not reopen)

1. Visibility: public ledger. Last five rounds. Six-character ids, new each episode.
2. Groups: both must nominate each other. A lone seat gets isolation, 0.8.
3. Units: y=1, r=1.6, isolation 0.8.
4. Before picture: `runs/pgg/frozen_qwen_qwen3.8-27b_choice_s8_t0.4_ledger_id6_probe_seed0_n5.jsonl`.
5. No reputation scalar and no game-theory jargon in prompts.
6. All model text enters the env only through `repair`.
7. A training reward is return from that round to the end of the episode.

## Exit criteria

- [x] Ledger probe file logged
- [x] `notes/t2-gate.md`
- [x] Return-to-go pilot logged. `runs/train/grpo_pilot_seed0.jsonl`
- [ ] A trained file compared with the frozen probe file
- [ ] Tracker marked FINISHED

## Log

| Block | Result |
|-------|--------|
| Probe file | Zero named 15/570 after round 0. 0.3 named 21/570. Model named model 1492/2850. |
| GRPO pilot | Five rounds, six model seats, four replies. 30 groups, 9 with spread, 21 skipped. Cost $0.21. Round 0 continuing actions had empty nominations, so round 1 working set was empty. Model contribution on the continuing action 0.4 to 0.8. Not a learning result. |

## Next

Do not read this file as a trained policy. A comparison needs a frozen file and a trained file on the same prompt path. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-05 ~02:47 EDT — pilot cost $0.21, 9 of 30 groups stepped. T2 not finished.
