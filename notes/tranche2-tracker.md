# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`
**Repo:** `N-T-SH/learned-reputation`
**Opened:** 2026-10-01

## Status
**OPEN, paused at end of 2 Oct.** Qwen N=4 temperature-0 run is finished and on `main`. Next session starts the N=8 temperature-0.4 frozen run. Do not open T3.

## Locks (do not reopen)

1. Visibility: local. Last working-set contributions, plus messages to me from the previous round.
2. Groups: both must nominate each other. One-sided nominate is not a pair.
3. Units: y=1, scripted threshold 0.5, r=1.6, isolation 0.8.
4. Finished Qwen file stays N=4, temperature 0. Next frozen run is N=8, temperature 0.4. A later trained run must match that.
5. No reputation scalar and no game-theory jargon in prompts.
6. All model text enters the env only through `repair`.

## Exit criteria

- [x] FakeLM smoke
- [x] OpenRouter smoke: Ling, 4 seats x 5 rounds, all replies ok
- [x] Prompt checklist committed. Sample `ok True ok`.
- [x] Partner-choice vs fixed-group logged. Ling working sets did not differ.
- [x] Reasoning toggle skipped as a study aim. Comparison model must still accept reasoning off.
- [x] Longer frozen run logged. `runs/pgg/frozen_qwen_qwen3-8b_choice_seed0_n10.jsonl`
- [ ] N=8, temperature 0.4, 5 episodes, same model, reasoning off
- [ ] Training pilot, or a clear failure report
- [ ] `notes/t2-gate.md` from real logs
- [ ] Tracker marked FINISHED

## Instructions

Do not edit `notes/2month-plan.md`. Sync from this file and `notes/for-plan-bot.md`.

Lab loop from 2 Oct: implementation bot writes the code, explains it, and asks a check question. Do not leave functions empty.

## Log

| Block | Result |
|-------|--------|
| T2-a | FakeLM smoke green. |
| Router | `openrouter/free` returned `User Safety: safe`. Gemma free was upstream 429. |
| T2-b | Checklist committed. Sample `ok True ok`. |
| T2-c | Ling choice and fixed. Both kept all four seats. |
| T2-d | Skipped. Not a study aim. |
| Comparison model | GPT-OSS rejected reasoning off. Qwen accepted `reasoning.enabled: false`. |
| Longer run | 10 episodes, 20 rounds, 800 replies, all ok. Temperature 0, so episodes repeated one path. Seat 3 out after round 1 in every episode. Isolation 0.8. Insiders about 1.42. Not a training result. |
| Flags | `--temperature` and `--seats` are on main. A new setting writes a new file. |
| T2-e | Not started. No local GPU. OpenRouter cannot fine-tune. |

## Next

```
python -m envs.pgg_scripted.run_frozen --speaker openrouter --model qwen/qwen3-8b --groups choice --seats 8 --temperature 0.4 --rounds 20 --episodes 5
```

Then go/no-go. Do not open T3.

---
**Signed:** Implementation bot — 2026-10-02 ~06:46 EDT — session closed. Resume at the N=8 temperature-0.4 command above. T2 not finished.
**Signed:** ReputationLearning — 2026-10-02 ~15:58 IST — one-line pointer: 2month-plan speed-run synced; no exit-criteria edits.
**Signed:** ReputationLearning — 2026-10-02 ~16:01 IST — pointer only: go/no-go + optional <$25 pilot after N=4 finish + N=8 frozen.
