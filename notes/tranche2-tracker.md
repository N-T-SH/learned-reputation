# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN.** Chat-prompt pilot parsed and took 16 steps. One episode is not a comparison. Do not open T3.

## Locks (do not reopen)

1. Visibility: public ledger. Last five rounds. Six-character ids, new each episode.
2. Groups: both must nominate each other. A lone seat gets isolation, 0.8.
3. Units: y=1, r=1.6, isolation 0.8.
4. Fireworks comparison prompt: ledger block as the user message, thinking off. Shared by `agents/train/prompt.py`.
5. No reputation scalar and no game-theory jargon in prompts.
6. All model text enters the env only through `repair`.
7. A training reward is return from that round to the end of the episode.

## Log

| Block | Result |
|-------|--------|
| Fireworks frozen chat | 30 of 30 ok. Zero named 9/30. 0.3 named 8/30. Model named model 45/150. Mean contribution 0.94. |
| Chat pilot | `runs/train/grpo_pilot_chat_seed0.jsonl`. 30 groups, 16 with spread, 0 repair failures. Zero named 9/30. 0.3 named 4/30. Model named model 26/150. Continuing contribution mostly 0.5. Rounds 0 and 1 had empty nominations, so the working set was empty through round 2. Not a learning result. |

## Next

Do not treat 4/30 against 8/30 as a trained change. A comparison needs a frozen file and a trained file that were not updated inside the same five rounds. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-05 ~03:56 EDT — chat pilot 16 of 30 groups stepped. T2 not finished.
