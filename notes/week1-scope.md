# Tranche 1 scope — scripted PGG pipeline
**Updated:** 2026-09-29 (after Lab lock)  
**Repo:** `N-T-SH/learned-reputation` (not `resilient-lab`)  
**Pacing:** calendar “weeks” in the 2-month plan map to **tranches**. A tranche is 2–3h AI+human blocks. Advance when the gate is green; do not wait out a calendar week.

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
