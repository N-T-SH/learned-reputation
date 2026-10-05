# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** Frozen probe file is the before picture. Fireworks GRPO smoke took one optimizer step. The study reward is not attached yet. Do not open T3.

## Locks (do not reopen)

1. Visibility: public ledger. Last five rounds of every seat's contribution and nominations. Six-character ids, new each episode.
2. Groups: both must nominate each other. A lone seat gets isolation, 0.8.
3. Units: y=1, r=1.6, isolation 0.8.
4. Before picture: `runs/pgg/frozen_qwen_qwen3.8-27b_choice_s8_t0.4_ledger_id6_probe_seed0_n5.jsonl`.
5. No reputation scalar and no game-theory jargon in prompts.
6. All model text enters the env only through `repair`.
7. A training reward must be return from that round to the end of the episode, not that round's payoff alone.

## Exit criteria

- [x] FakeLM smoke
- [x] OpenRouter smoke
- [x] Ledger probe file logged
- [x] `notes/t2-gate.md`
- [x] Fireworks GRPO plumbing smoke. One step, stand-in reward.
- [ ] Training pilot with return-to-go, or a clear failure report
- [ ] Tracker marked FINISHED

## Log

| Block | Result |
|-------|--------|
| Probe file | Zero seat named 15/570 after round 0. 0.3 seat named 21/570. Model seats named each other 1492/2850. Not a training result. |
| GRPO smoke | Qwen 3.8 27B, chat template, thinking off. Four short JSON replies. Scores 0.5, 0.5, 0.5, 0.95. Advantages about -0.11, -0.11, -0.11, 0.34. `step_ok ForwardBackwardOutput`. Reward was the contribute number, not episode return. |

## Next

Attach the game return to this loop. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-05 ~02:05 EDT — one GRPO step completed on a stand-in score. T2 not finished.
