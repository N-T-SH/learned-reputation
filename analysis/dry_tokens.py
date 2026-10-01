"""Dry event view. No model. Messages are for next round, not this c."""

# Rough: ~4 chars per token. Good enough for a T1-d number.

def event_view(seat: int, working: list[int], last_c: dict[int, float], inbox: list[str]) -> str:
    lines = [
        f"You are seat {seat}.",
        "You see only your last working set. No global ledger.",
        "Messages below arrived from the previous round.",
        "Reply with message, nominate, contribute in [0, 1].",
        "Last visible contributions:",
    ]
    for j in working:
        lines.append(f"  seat {j}: c={last_c.get(j)}")
    lines.append("Inbox:")
    lines.extend(f"  {m}" for m in inbox) if inbox else lines.append("  (none)")
    return "\n".join(lines)


if __name__ == "__main__":
    text = event_view(
        seat=0,
        working=[0, 1, 2],
        last_c={0: 1.0, 1: 0.0, 2: 1.0},
        inbox=["seat 1: I kept my unit"],
    )
    n_chars = len(text)
    print(text)
    print("---")
    print(f"chars={n_chars} rough_tokens={n_chars / 4:.0f}")
    print("episode_x4_seats_x20_rounds", int(n_chars / 4 * 4 * 20))
