# Locked (T0 → T1)

- Visibility: **local**.
- Groups: **bilateral form / unilateral break** (mutual nominate).
- Units: **y = 1**, threshold **0.5**, r = 1.6, isolation = 0.8.
- N = 4 until `include_next` works, then N = 6.
- Repo: `learned-reputation`.
- Positive: include j next round iff last visible c_j ≥ 0.5 (None → include).
- Null: random include each round; ignore history.
- Withhold: reputation scalar, update, gossip-into-score, score-coupled connect, the word REPUTATION in prompts.
