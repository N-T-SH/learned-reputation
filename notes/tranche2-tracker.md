# T2 tracker — frozen LLM seats + train pilot
**Path:** `notes/tranche2-tracker.md`  
**Repo:** `N-T-SH/learned-reputation`  
**Opened:** 2026-10-01 (after T1 finished)  
**Pacing:** tranches, not calendar weeks.

## Status
**OPEN, paused at end of 1 Oct Lab.** T2-a is green with FakeLM, not a model. T2-b is scaffolded and not filled. No GRPO this tranche. T2 is not finished.

## Tranche map

| Old week | Tranche | Status |
|----------|---------|--------|
| 0 | T0 | Closed 29 Sep |
| 1–2 | T1 | **Finished** 1 Oct (`notes/tranche1-tracker.md`) |
| 3–5 | **T2** | **Active, paused** |
| 6–9 | T3 | After T2-end go/no-go |
| 10–12 | T4 | If main result positive |

## Locks (carry from T1 — do not reopen)

1. Visibility: **local** — last working-set partners' `c`, plus messages to me (prior round). Not a global ledger.
2. Groups: **bilateral form / unilateral break.**
3. Units: y=1, threshold 0.5 (scripted control only), r=1.6, isolation 0.8.
4. Start frozen runs at **N=4**. N=6 optional; N=16 only after plan says so.
5. Repo: `learned-reputation` only.
6. Withhold: reputation scalar, score update, gossip-into-score, score-coupled connect, the word REPUTATION and game-theory jargon in prompts.
7. All model text enters the env only via `repair()`. Bad text becomes an empty action and a logged failure.

## Exit criteria (T2)

- [x] Frozen smoke: 5 rounds, N=4, all seats through `repair`, `runs/pgg/frozen_smoke_seed0.jsonl`. Speaker is FakeLM.
- [ ] Prompt + obs builder: local visibility; prior-round messages; no forbidden vocab
- [ ] Partner-choice on vs fixed-group
- [ ] Reasoning on/off, or a signed blocker if the provider cannot toggle
- [ ] Training pilot, or a clear failure report
- [ ] `notes/t2-gate.md` from real logs only
- [ ] Tracker marked FINISHED

## Instructions for implementation bot

**Read first (do not edit):** `notes/2month-plan.md`, `notes/locked-controls.md`, closed `notes/tranche1-tracker.md`.
**Co-edit + sign:** this file.
**Code you own:** `envs/`, `runs/`, `agents/`, `train/`, prompt modules.

### T2-b — prompts
Prompt states affordances only. Never tell the model to build reputation, exclude free-riders, or name REPUTATION. Observation is local last working-set `c` and messages to this seat from the previous round. Still run `repair` on everything. Checklist fails if forbidden strings appear.

### T2-c — partner choice contrast
Condition A: nominations go through `form_groups`. Condition B: ignore nominations and use a pre-set working set. Same speaker. Short runs. Write both JSONLs.

### T2-d — reasoning on/off
If the provider can toggle reasoning, run twice. If not, sign a blocker. Do not block T2-e on it.

### T2-e — train pilot
Shared policy, reasoning off. About 200 episodes, or fewer if budget is tight and the count is written down. Do not claim emergence. Draft `notes/t2-gate.md` from real logs only.

### Out of T2
Full GRPO campaign, reintegration probe, hardcoded reputation score.

## Log

| Block | Result |
|-------|--------|
| T2-a | Green. FakeLM, 5 rounds, all `ok` true. Seat 0 text had `[0, 0]`; repair kept `[0]`. Everyone contributed 1, payoff 1.6. Not a model result. |
| T2-b | Scaffold `analysis/prompt_check.py` is on main. `prompt_is_ok` was not filled this session. |
| T2-c | not started |
| T2-d | not started |
| T2-e | not started |

## Session close — 1 Oct

Stopped at Nitesh's request, before the 15:30 hard stop. Done today: T1-d closed earlier (repair smoke, bad-action row, dry tokens about 5540 per episode); T2 opened; T2-a FakeLM loop green. Not done: prompt checklist, provider choice, partner-choice contrast, reasoning toggle, train pilot. Resume at `prompt_is_ok` in `analysis/prompt_check.py`, then `python -m analysis.prompt_check`.

## Next

Next session: fill `prompt_is_ok`. Provider choice still with Nitesh. Do not open T3.

---
**Signed:** ReputationLearning — 2026-10-01 ~10:55 IST — opened T2.
**Signed:** Implementation bot — 2026-10-01 ~11:25 IST — T2-a green on FakeLM smoke.
**Signed:** Implementation bot — 2026-10-01 ~15:05 IST — session closed. T2-a green. T2-b not filled. T2 not finished.
