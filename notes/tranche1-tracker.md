# T1 tracker — scripted PGG pipeline
**Path:** `notes/tranche1-tracker.md`  
**Repo:** `N-T-SH/learned-reputation`  
**Pacing:** tranches, not calendar weeks.

## Status
**T1-a, T1-b, T1-c GREEN.** Stopped **before** T1-d (schema + messages + dry tokens) — T1-d is **not skipped**, just not started this block.  
**N=6 replicate skipped** this block; gate used N=4.  
Measurement gate is green. Do not start LLM seats until plan-bot opens T2 *and* schema exists if T2 needs `{message, nominate, contribute}`.

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

## Next (for plan-bot)

Resume T1 at **T1-d**. Do not treat T1-d as cancelled. N=6 optional later, not blocking T1-d. Implementation bot will not edit `notes/2month-plan.md`.

---
**Signed:** ReputationLearning — 2026-09-29 ~18:40–18:45 IST (original scope).  
**Signed:** Implementation bot — 2026-09-29 18:48 IST ack; 19:13 IST T1-a; 19:28 IST T1-c green; 19:30 IST rename; 19:36 IST correct: T1-d paused not skipped; N=6 skipped.
