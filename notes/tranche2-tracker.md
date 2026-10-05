# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** Frozen-prompt pilot parsed poorly. Not a comparison with the OpenRouter file. Do not open T3.

## Locks (do not reopen)

1. Visibility: public ledger. Last five rounds. Six-character ids, new each episode.
2. Groups: both must nominate each other. A lone seat gets isolation, 0.8.
3. Units: y=1, r=1.6, isolation 0.8.
4. Before picture: `runs/pgg/frozen_qwen_qwen3.8-27b_choice_s8_t0.4_ledger_id6_probe_seed0_n5.jsonl`.
5. No reputation scalar and no game-theory jargon in prompts.
6. All model text enters the env only through `repair`.
7. A training reward is return from that round to the end of the episode.
8. A trained file must use the frozen prompt block. No system line.

## Exit criteria

- [x] Ledger probe file logged
- [x] `notes/t2-gate.md`
- [x] Frozen-prompt pilot logged. `runs/train/grpo_pilot_frozenprompt_seed0.jsonl`
- [ ] A trained file whose replies parse, compared with the frozen probe file
- [ ] Tracker marked FINISHED

## Log

| Block | Result |
|-------|--------|
| Probe file | OpenRouter. Zero named 15/570 after round 0. 0.3 named 21/570. Model named model 1492/2850. |
| Wrapped pilot | Chat template. 9 of 30 groups stepped. Cost $0.21. Not comparable. |
| Frozen-prompt pilot | Same words as the frozen file. 14 of 30 groups stepped. 13 of 30 continuing actions were the repair failure: empty nomination, contribution 0. Round 1 working set was empty. Not a learning result. |

## Next

The plain block does not parse on this Fireworks sampler. Do not compare it with the OpenRouter file. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-05 ~03:15 EDT — frozen-prompt pilot mostly failed repair. T2 not finished.
