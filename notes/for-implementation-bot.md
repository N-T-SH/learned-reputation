# For the implementation bot

> **Round closed 8 Oct 2026; T3 NO-GO.** No active work. The "Active work" section below is historical; the standing rules still apply to any new round. Index: `notes/README.md`.

**Repo:** `N-T-SH/learned-reputation`  
**Updated:** 2026-10-01

## What you own
- `envs/`, `runs/`, README run instructions, `agents/` / `train/` as you add them, tests that prove gates.
- In-loop with Nitesh on named cruxes and provider choice (API / FakeLM / vLLM).

## What you read (do not edit)
- **`notes/2month-plan.md`** — **Read-only.** ReputationLearning alone updates it.
- `notes/archive/superseded/locked-controls.md` — do not reopen.
- Closed trackers (e.g. `notes/archive/trackers/tranche1-tracker.md`) — history only.

## Active work
- **Now:** `notes/tranche2-tracker.md` — start at **T2-a**. Follow the “Instructions for implementation bot” section there (detailed).
- Pull → code → update tracker Log/Exit criteria → **sign at bottom** → push.

## When a tranche is finished
1. Mark the tracker **FINISHED** in Status with a signed line.
2. Do **not** invent the next tracker yourself.
3. ReputationLearning generates `notes/tranche{N+1}-tracker.md` and syncs the 2-month plan.

## Standing rules
1. Always `git pull --ff-only` before you edit.
2. All model output enters the env only through `schema.repair` (or its successor module).
3. No REPUTATION / exclude-verb / game-theory jargon in prompts.
4. Advance on finished marks, not calendar weeks.
5. Hours / Lab calendar: Coach — do not invent hour totals.

---
**Signed:** ReputationLearning — created 2026-09-29 ~18:45 IST.  
**Signed:** ReputationLearning — updated 2026-09-29 ~19:40 IST (tracker rename; finish → next-tranche handoff).  
**Signed:** ReputationLearning — updated 2026-10-01 ~10:55 IST (T1 closed; T2 active).  
**Signed:** ReputationLearning — 2026-10-08 ~15:55 IST — Round-closed banner added; archived links updated. Kept at this path because `skills/lab-coordination/SKILL.md` names it.
