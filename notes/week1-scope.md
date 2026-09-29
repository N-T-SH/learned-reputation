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
- [ ] `include_next` implemented (positive + null)
- [ ] JSONL: per round c_i, working set, payoffs
- [ ] Positive: include j iff last visible c_j ≥ 0.5 (None → include)
- [ ] Null: random nominate each round; regression ~0
- [ ] Schema {message, nominate, contribute} when accelerating
- [ ] Dry tokens/episode (no vLLM required)

## Blocks

| Block | Crux | Done when |
|-------|------|-----------|
| T1-a | `include_next` | JSONL for positive + null |
| T1-b | confirm `form_groups` | mutual → together; one-sided → not |
| T1-c | inclusion ~ last c | β positive on script; ~0 on null |
| T1-d (if time) | schema + messages + token count | malformed logged |

## Coordination (ReputationLearning)

**Owners**
- **ReputationLearning:** `notes/` planning — keeps `notes/2month-plan.md` in sync; co-edits this tranche scope/log. Always `git pull` before edit; **sign at bottom**; push.
- **Implementation bot:** `envs/`, `runs/`, README. Co-edits **this** tranche scope/log (progress, blockers) and **signs at bottom**. Reads `notes/2month-plan.md` for context — **does not edit the 2-month plan** (see `notes/for-implementation-bot.md`). Does not reopen locks in §Locked / `notes/locked-controls.md`.

**Block order (do not skip the gate)**
1. **T1-a** — implement `include_next` (positive + null); emit JSONL under `runs/pgg/`.
2. **T1-b** — confirm working-set rule matches lock (mutual nominate → together; one-sided → not). Treat as verify against env, not a redesign.
3. **T1-c** — inclusion ~ last visible `c` regression: β recoverable on positive; ~0 on null. **This is the T1 gate.**
4. **T1-d** — only if T1-c is green *or* leftover block time after a–c; schema `{message, nominate, contribute}` + dry token count. Malformed → logged, not silent.

**Artifacts that prove the gate (paths)**
- `runs/pgg/positive_seed0.jsonl` and `runs/pgg/null_seed0.jsonl` (or agreed seed set)
- Short regression summary (β₁/β₂ or agreed coefficients + null check) pointed from a future `notes/t1-gate.md` when green — do not invent numbers here.

**Advance rule**
- Exit criteria checkboxes above all green → open **T2** scope note (frozen seat + train pilot). Do not start LLM seats inside T1.
- Calendar week labels in the old 2-month plan are informational only; **advance on gate**, not on Sunday.

**Carry-forward (non-blocking)**
- Local vLLM serve remains a known blocker (no GPU). Dry token accounting in T1-d is enough; real serve is not a T1 exit item.

**Out of T1 (do not pull in)**
- GRPO training runs, N=16 as default, reintegration, tabular Ueshima recreate as product, RepuNet scalar / gossip / score-coupled connect, the word REPUTATION in prompts.

---
**Signed:** ReputationLearning — updated 2026-09-29 ~18:40 IST (planning pass after Nitesh Lab lock + pull).
**Signed:** ReputationLearning — updated 2026-09-29 ~18:45 IST (joint scope/log signing; link `notes/2month-plan.md` + `notes/for-implementation-bot.md`).

