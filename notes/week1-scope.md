# Tranche 1 scope — scripted PGG pipeline
**Updated:** 2026-09-29 (Lab lock; dual-sign + 2-month plan link)  
**Repo:** `N-T-SH/learned-reputation` 
**Pacing:** calendar “weeks” in the 2-month plan map to **tranches**. A tranche is multiple 2–3h AI+human blocks. Advance when the gate is green; do not wait out a calendar week.

## Tranche map (old week labels)

| Old plan week | Tranche | Status |
|---------------|---------|--------|
| 0 reading / concepts | **T0** | Closed 29 Sep |
| 1–2 env, schema, scripted ±, regression | **T1** | Active — accelerate; schema + messages + regression in the same tranche if time |
| 3–5 frozen runs + train pilot | **T2** | After T1 gate |
| 6–9 full GRPO if Week-5 go | **T3** | Funding/tech gate |
| 10–12 reintegration + write-up | **T4** | If main result positive |

## Locked this Lab (do not reopen)

1. **Visibility:** local — last working-set partners’ c, plus later messages *to me*. Not a global ledger.
2. **Group rule:** **bilateral form / unilateral break.** Co-membership next round iff **both** nominate each other. One-sided nominate → no shared work.
3. **Units:** y = E = 1. Threshold **0.5**. r=1.6. Isolation 0.8. Do **not** use E=10 / threshold 5 in this repo.
4. **N:** start **4** until `include_next` runs; then **N=6** for the regression gate. N=16 only after that.
5. **Repo:** `learned-reputation` only.

## Thesis (T1)

Smallest runnable loop that proves the measurement pipeline **before any LLM seat**: env step → logs → inclusion regression. Schema + messages in the same tranche if time.

## Exit criteria (T1)

- [ ] Mutual nominate → same working set; linear PGG (y=1, r=1.6)
- [x] `include_next` implemented (positive + null) — Nitesh 29 Sep; JSONL wrote
- [x] JSONL: per round c_i, working set, payoffs (noms field added in run_controls after first run — re-run)
- [ ] Positive: include j iff last visible c_j ≥ 0.5 (None → include)
- [ ] Null: random nominate each round; regression ~0
- [ ] Schema {message, nominate, contribute} when accelerating
- [ ] Dry tokens/episode (no vLLM required)

## Blocks

| Block | Crux | Done when |
|-------|------|-----------|
| T1-a | `include_next` | JSONL for positive + null — **done** |
| T1-b | confirm `form_groups` | mutual → pair; one-sided → not a pair |
| T1-c | inclusion ~ last c | β positive on script; ~0 on null |
| T1-d (if time) | schema + messages + token count | malformed logged |

## Coordination (ReputationLearning)

**Owners**
- **ReputationLearning:** `notes/` planning — keeps `notes/2month-plan.md` in sync; co-edits this tranche scope/log. Always `git pull` before edit; **sign at bottom**; push.
- **Implementation bot:** `envs/`, `runs/`, README. Co-edits **this** tranche scope/log (progress, blockers) and **signs at bottom**. Reads `notes/2month-plan.md` for context — **does not edit the 2-month plan**. Does not reopen locks.

**Block order (do not skip the gate)**
1. **T1-a** — **done** (JSONL wrote; last working all-in is not the gate).
2. **T1-b** — `python -m analysis.check_form_groups` after pull.
3. **T1-c** — outcome is **nominate / mutual pair**, not “j in working” (self-nom always keeps solos in working).
4. **T1-d** — after T1-c or leftover time.

**Artifacts that prove the gate (paths)**
- `runs/pgg/positive_seed0.jsonl` and `runs/pgg/null_seed0.jsonl`
- After pull+re-run, those files include `noms`.

**Implementation status**
- T1-a green. T1-b next. No LLM seats.

---
**Signed:** ReputationLearning — updated 2026-09-29 ~18:40 IST.
**Signed:** ReputationLearning — updated 2026-09-29 ~18:45 IST.
**Signed:** Implementation bot — 2026-09-29 18:48 IST — ack for-implementation-bot.md.
**Signed:** Implementation bot — 2026-09-29 19:13 IST — T1-a JSONL wrote; last working [0,1,2,3] both modes (not the metric). Added noms to JSONL + check_form_groups.py.
