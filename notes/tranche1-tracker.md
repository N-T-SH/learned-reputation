# T1 tracker — scripted PGG pipeline
**Path:** `notes/tranche1-tracker.md`  
**Repo:** `N-T-SH/learned-reputation`  
**Pacing:** tranches, not calendar weeks.

## Status
**T1-a through T1-d are done** (Thu 1 Oct). N=6 was skipped on purpose. No model seats yet. T2 is not opened; plan-bot opens that tracker only if Nitesh marks T1 finished.

## Locks

1. Visibility: local. A seat sees last working-set contributions and messages to them, not a global ledger.
2. Groups: both must nominate each other. One-sided nominate does not make a pair.
3. Units: endowment 1, include if last visible contribution is at least 0.5, multiplier 1.6, isolation payoff 0.8.
4. Gate run used 4 seats. Six-seat rerun skipped.
5. Bad model text becomes no message, no nominations, contribution 0, and a logged failure. A well-typed action can drop a duplicate or an illegal id and still count.
6. Messages in the prompt are from the previous round.

## Log

| Block | Result |
|-------|--------|
| T1-a/b/c | Done. Scripted rule always nominates a high contributor and never a low one. Random nominations stay near a coin flip. |
| T1-d repair | Good action kept nominations 0 and 1. A raw string failed closed. |
| T1-d tokens | One seat view about 69 tokens. Four seats for 20 rounds about 5540 prompt tokens per episode. Rough chars/4 estimate, input only. |
| T1-d bad row | `runs/pgg/schema_bad.jsonl`: raw string, ok false, empty message, empty nominations, contribution 0. |

## Exit criteria

- [x] Scripted measurement gate
- [x] Repair smoke
- [x] Bad action row logged
- [x] Dry tokens/episode about 5540 at 4 seats, 20 rounds
- [ ] Six-seat rerun — skipped

---
**Signed:** Implementation bot — 2026-10-01 ~10:50 IST — T1-d closed. Bad action file confirmed. T2 not opened.
