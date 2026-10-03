# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** Ledger plus scripted free rider is the before picture. The model almost never named the seat that contributed 0. Train decision still open. Do not open T3. Do not train against the older no-ledger file.

## Locks (do not reopen)

1. Visibility: public ledger. Last five rounds of every seat's contribution and nominations. Labels shuffled per episode. Log keeps real ids.
2. Groups: both must nominate each other. One-sided nominate is not a pair. A lone seat gets isolation, 0.8.
3. Units: y=1, r=1.6, isolation 0.8.
4. Before picture for a 27B pilot: `runs/pgg/frozen_qwen_qwen3.8-27b_choice_s8_t0.4_ledger_fr_seed0_n5.jsonl`. Same model, temperature 0.4, reasoning off, free rider on.
5. No reputation scalar and no game-theory jargon in prompts.
6. All model text enters the env only through `repair`.
7. A training reward must be return from that round to the end of the episode, not that round's payoff alone.

## Exit criteria

- [x] FakeLM smoke
- [x] OpenRouter smoke
- [x] Prompt checklist committed
- [x] Partner-choice vs fixed-group logged
- [x] Reasoning off on the comparison model
- [x] Ledger free-rider file logged
- [ ] Training pilot, or a clear failure report
- [ ] `notes/t2-gate.md` from the ledger file
- [ ] Tracker marked FINISHED

## Log

| Block | Result |
|-------|--------|
| Earlier frozen | No-ledger files left seats out without a contribution below 0.5. Seat 7 out 83/100 on the 27B file. That was position. |
| Ledger + free rider | 100 rows, 800 replies, all ok. 2232 seconds. Seat 7 scripted, contribution 0. In the working set 8/100 rounds. Named by a model seat 7/700 times, and 3/665 after round 0. Model contributions 0.5 to 1.0, mean 0.83. Shown-label out rates still uneven (label 6 out 77/100, labels 0 and 5 out 22/100). Not a training result. |
| OpenRouter bill | $0.23 after the no-ledger 27B file. This file is extra. |
| T2-e | Not started. Reward must be return-to-go. |

## Next

Write `notes/t2-gate.md` from the ledger file. Then the train-or-not call. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-03 ~06:00 EDT — ledger free rider almost never named. T2 not finished.
**Signed:** ReputationLearning — 2026-10-02 ~15:58 IST — one-line pointer: 2month-plan speed-run synced; no exit-criteria edits.
**Signed:** ReputationLearning — 2026-10-02 ~16:01 IST — pointer only: go/no-go + optional <$25 pilot after N=4 finish + N=8 frozen.
