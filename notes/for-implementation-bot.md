# For the implementation bot

**Repo:** `N-T-SH/learned-reputation`  
**Updated:** 2026-09-29

## What you own
- `envs/`, `runs/`, README run instructions, tests that prove gates.
- In-loop with Nitesh on named cruxes (e.g. `include_next`).

## What you read (do not edit)
- **`notes/2month-plan.md`** — tranche map, scientific targets, non-goals, calendar ceiling. **Read-only.** ReputationLearning alone updates and signs that file. If something in the plan conflicts with Lab reality, leave a signed note on the **active tranche tracker** (do not patch the 2-month plan yourself).
- `notes/locked-controls.md` — do not reopen.

## What you co-own (edit + sign)
- Active tranche tracker: `notes/tranche{N}-tracker.md` (currently `notes/tranche1-tracker.md`). Pull first; update Status / Log / Exit criteria / blockers; **append a signed line at the bottom** (`Implementation bot — YYYY-MM-DD HH:MM IST — …`); push.
- ReputationLearning does the same for coordination and plan sync.

## When a tranche is finished
1. Mark the tracker **finished** in Status (and check exit criteria) with a clear signed line.
2. Do **not** invent the next tracker yourself.
3. ReputationLearning will generate `notes/tranche{N+1}-tracker.md` in the **same format** and sync `notes/2month-plan.md`.
4. Follow the new tracker once it lands on `main`.

## Standing rules
1. Always `git pull --ff-only` before you edit notes or code that others may have touched.
2. Do not start LLM seats until the active tranche allows it (see tracker Status + 2-month plan).
3. Advance on gate / finished mark, not on calendar week labels.

---
**Signed:** ReputationLearning — created 2026-09-29 ~18:45 IST.  
**Signed:** ReputationLearning — updated 2026-09-29 ~19:40 IST (tracker rename; finish → next-tranche handoff).
