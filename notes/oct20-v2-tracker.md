# Oct 20 v2 tracker: instrument fix, then four episodes

**Repo:** `N-T-SH/learned-reputation`
**Pre-registration:** unchanged, `878692c` in `notes/prereg-2026-10-20.md`. Do not edit it.
**Status:** V2-a done. Waiting on the rules text before V2-b.
**Deadline:** report pushed by 00:30 IST on 21 Oct.
**Cap:** about $1 for this tracker. Stop if the running total for the 20 Oct round passes $8.

## Why there is a v2

The 20 Oct game files are scored correctly, and the audit found no role bug. They still cannot be read as partner choice, for two reasons.

1. The seat prompt never states the rules. `prompt_for` in `envs/pgg_scripted/run_frozen.py` says only "nominate partner ids, and set contribution". It does not say that a pair needs both names, that the pot is multiplied by 1.6, or that a seat in no pair gets 0.8. The design note has those rules. The model never saw them.
2. Without the rules, "nominate" is ambiguous. In `full_s0` and `full_s1` every model seat named the zero seat, with messages such as "Solidarity against the free rider" and "Cooperate fully. Nominate ex4i9b." The seats used the word to flag a seat, not to pick a partner. Contributions near 1.0 and five or six names per reply fit the same reading: with no stated cost, naming everyone and giving everything looks harmless.

There is also a pairing fault. `episode_ids` builds a `set` and then shuffles it. Set order depends on the process hash seed, so the same seed gave a different id order, and different role seats, in each arm. The 8 Oct seed-40 files are not affected, because they share a stored id list.

This is a logged instrument fix, not a rerun to change a result. Commit this tracker and the code change before any paid call.

## Steps

### V2-a: prompt, schema and ids (no paid calls)

Done. See Log.

### V2-b: four episodes (about $0.50)

Same settings as 20 Oct otherwise: Qwen 3.8 27B on Fireworks, thinking off, temperature 0.4, 24 rounds, 5 model seats plus reformer, steady and zero, "Play may end after any round." File names end in `_v2`.

| Arm | memory | group rule | seeds |
|---|---|---|---|
| window | 5 | choice | 0, 1 |
| full | 24 | choice | 0, 1 |

**Parse gate:** run `window_s0_v2` first. Stop the game runs if more than 15 of the first 50 model replies fail repair. Report the failure types and stop.

**Sanity line, reported but not a gate:** in both window episodes, print how often the steady seat and the zero seat are named in rounds 1 to 8. The 8 Oct frozen file had the steady-style seat far above the zero. Record what v2 shows; do not change anything because of it.

### V2-c: report

Write `notes/report-2026-10-20-v2.md` in the same layout as `notes/report-2026-10-20.md`:

1. The per-episode table: reformer, steady and zero named out of 80 after round 8; latency; mean contribution; partners per reply; repair failures.
2. The forgiveness gap by round.
3. The T1 table.
4. Three raw messages per episode from round 15, quoted whole.
5. The pre-registered predictions P1, P3, P4, T1 and T2, each marked held, failed or unclear, with the deciding number. T3 is not tested in v2, because there is no fixed arm.

Then append a short section to `notes/for-plan-bot-2026-10-20.md`: the dollar total, and one line per arm stating what the file showed. Add no interpretation beyond held, failed or unclear.

## Rules for this tracker

- `git pull --ff-only` before every edit.
- Do not touch the 20 Oct files, `runs/train/`, adapters, or the pre-registration.
- No reruns of v2 cells except for a logged infrastructure failure.
- Sign each step below when it is done, and push.

## Log

(implementation bot)

### V2-a done, 20 Oct 2026

- Rules block is in `rendered_prompt_v2`. `prompt_for` is unchanged.
- `repair` reads `partners` when `nominate` is absent. The env still stores `nominate`.
- `episode_ids_stable` sorts before the shuffle. Used only by `oct20_game.py`.
- Full reply is logged as `text`. Files will end in `_v2`.
- `python -m agents.probes.oct20_game --check` printed `word_check_ok`, `ids_stable`, and `check_ok`.

Window-5 prompt, round 3, seat `ojtk7t`, seed 0:

```
You are seat ojtk7t.
Rules. Each round every seat has one unit and chooses how much of it to put in, from 0 to 1.
Under partners, list the seats you want to work with. A pair forms only when both seats list each other.
Every seat in at least one pair joins the working group for that round.
The working group's inputs are added, multiplied by 1.6, and shared equally among its members.
A member also keeps whatever it did not put in. A seat in no pair gets 0.8 for the round.
Reply with a JSON object with keys message, partners, contribute.
Recent rounds, newest last. c is contribution. partners is who that seat listed.
  round 1
    seat idm3dl: c=1.0 partners=[]
    seat s3kn51: c=1.0 partners=[]
    seat uhquj6: c=1.0 partners=[]
    seat 7g0duv: c=1.0 partners=[]
    seat 37cpsn: c=1.0 partners=[]
    seat 7eknaf: c=1.0 partners=[]
    seat ojtk7t: c=1.0 partners=[]
    seat iwr2b7: c=1.0 partners=[]
  round 2
    (same eight seats, c=1.0, partners=[])
  round 3
    (same eight seats, c=1.0, partners=[])
Messages from the previous round:
  (none)
Play may end after any round.
Reply with only the JSON object. partners is a list of seat ids. contribute is a number. Keep the message under ten words.
```

Waiting on Nitesh: is the rules text acceptable as written? No paid call until yes.

---
**Signed:** ReputationLearning, 2026-10-20 ~22:05 IST. Opened v2: rules in prompt, `partners` key, stable ids, full-reply logging, four episodes.
**Signed:** implementation bot, 2026-10-20. V2-a done. Waiting on the rules text before V2-b.
