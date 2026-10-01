# T1 tracker — scripted PGG pipeline
**Path:** `notes/tranche1-tracker.md`  
**Repo:** `N-T-SH/learned-reputation`  
**Pacing:** tranches, not calendar weeks.

## Status
**T1-a, T1-b, T1-c GREEN.** Stopped **before** T1-d (schema + messages + dry tokens) — T1-d is **not skipped**, just not started this block.  
**N=6 replicate skipped** this block; gate used N=4.  
Measurement gate is green. Do not start LLM seats until plan-bot opens T2 *and* schema exists if T2 needs `{message, nominate, contribute}`.


## Today’s Lab wedge (Thu 1 Oct)

- **Window:** 10:00–15:30 IST (Coach). Hard stop 15:30 — Send Rent 16:30; Revise ML / CS329A 17:00–19:30 (do not steal study).
- **Main work:** **T1-d** — schema `{message, nominate, contribute}` + dry tokens/episode. Malformed → logged, not silent.
- **Owners:** Implementation bot + Nitesh in-loop on code; ReputationLearning = notes / plan sync only.
- **Out of wedge:** LLM seats, N=16, GRPO, reopening locks. N=6 replicate still optional / not blocking T1-d.
- When T1-d exit boxes are green and you mark T1 **finished**, ReputationLearning opens `notes/tranche2-tracker.md`.

## Tranche map

| Old week | Tranche | Status |
|----------|---------|--------|
| 0 | T0 | Closed 29 Sep |
| 1–2 | **T1** | a–c green; d **not started** |
| 3–5 | T2 | Not opened |
| 6–9 | T3 | After T2 go/no-go |
| 10–12 | T4 | If main result positive |

## Locks (do not reopen)

1. Visibility: **local**
2. Groups: **bilateral form / unilateral break**
3. Units: **y=1**, threshold **0.5**, r=1.6, isolation 0.8
4. Gate run at **N=4**. N=6 was planned after `include_next`; **skipped this block**.
5. Repo: `learned-reputation`

## Log

| Block | Result |
|-------|--------|
| T1-a | `include_next` on main (`6c240f1`). JSONL wrote both modes. |
| T1-b | `check_form_groups`: pairs `[(0, 1)]` then `[]`. Working set can still list solos. |
| T1-c | seed0 N=4 rates below. Gate **green**. |
| N=6 | **Skipped** this block. |
| T1-d | **Not started** (paused). Next T1 item when we resume. |

### T1-c rates (seed 0, N=4)

| file | n high / low c | P(nom \| c≥0.5) | P(nom \| c<0.5) |
|------|----------------|-----------------|-----------------|
| `runs/pgg/positive_seed0.jsonl` | 252 / 96 | **1.0** | **0.0** |
| `runs/pgg/null_seed0.jsonl` | 228 / 120 | 0.526 | 0.408 |

Positive recovers the planted threshold. Null is near coin-flip (small gap, one seed). Outcome is **nomination**, not “j in working.”

## Exit criteria

- [x] Mutual nominate → pair (T1-b)
- [x] `include_next` + JSONL
- [x] Positive rule recovered (N=4)
- [x] Null not recovered as a threshold (N=4)
- [ ] N=6 replicate — **skipped this block**
- [ ] Schema `{message, nominate, contribute}` — **not started**
- [ ] Dry tokens/episode — **not started** (T1-d)

## Next

**Now (Thu Lab):** T1-d only. Implementation bot will not edit `notes/2month-plan.md`. N=6 optional later, not blocking T1-d. Mark T1 finished when T1-d exit criteria are done (N=6 may stay unchecked as skipped).

---
**Signed:** ReputationLearning — 2026-09-29 ~18:40–18:45 IST (original scope).  
**Signed:** Implementation bot — 2026-09-29 18:48 IST ack; 19:13 IST T1-a; 19:28 IST T1-c green; 19:30 IST rename; 19:36 IST correct: T1-d paused not skipped; N=6 skipped.
**Signed:** ReputationLearning — 2026-09-29 ~19:40 IST ack: tracker is canonical (week1-scope retired); T1 still open at T1-d; will open T2 tracker only when you mark T1 finished.
**Signed:** ReputationLearning — 2026-10-01 ~10:15 IST Coach Lab live: T1-d wedge 10:00–15:30; hard stop before Rent/ML.
