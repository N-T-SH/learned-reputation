# T1 tracker — scripted PGG pipeline
**Path:** `notes/tranche1-tracker.md`  
**Repo:** `N-T-SH/learned-reputation`  
**Pacing:** tranches, not calendar weeks.

## Status
**T1-a, T1-b, T1-c GREEN.** T1-d almost closed (Thu 1 Oct).  
Dry tokens written. Bad-action JSONL not confirmed in chat.  
**N=6 skipped.** No LLM seats. T2 not opened.

## Locks

1. Visibility: **local**
2. Groups: **bilateral form / unilateral break**
3. Units: **y=1**, threshold **0.5**, r=1.6, isolation 0.8
4. N=4 gate. N=6 skipped.
5. Schema repair: drop duplicate and out-of-range ids; whole action fails on non-dict, bad types, or c outside [0, 1]. Failure is empty message, empty noms, c=0, ok=False.
6. Messages in the prompt are from the **previous** round.

## Log

| Block | Result |
|-------|--------|
| T1-a/b/c | Green. Positive P(nom\|c≥0.5 / c<0.5)=1.0/0.0; null 0.526/0.408. |
| T1-d repair | Smoke green. Illegal id dropped. Bad string → empty action. |
| T1-d tokens | Example view 277 chars, ~69 tokens. N=4 × R=20 ≈ **5540** prompt tokens/episode (chars/4, no model). |
| T1-d bad JSONL | Not confirmed. |

## Exit criteria

- [x] T1-a/b/c
- [x] `repair` smoke
- [ ] Bad action row in `runs/pgg/schema_bad.jsonl`
- [x] Dry tokens/episode ≈ 5540 at N=4, R=20
- [ ] N=6 — skipped

---
**Signed:** Implementation bot — 2026-10-01 ~10:45 IST — dry token count logged; schema_bad.jsonl still unchecked.
