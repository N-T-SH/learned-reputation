"""T2-b checklist. Fail if a prompt teaches the game or shows the whole population."""

from envs.pgg_scripted.run_frozen import prompt_for

FORBIDDEN = (
    "reputation",
    "exclude",
    "free-rider",
    "free rider",
    "public good",
    "nash",
    "defect",
    "cooperate",
)


def prompt_is_ok(text: str, visible_ids: set[int], n_seats: int) -> tuple[bool, str]:
    """Return (ok, reason).

    Fail if any forbidden word appears, ignoring case.
    Fail if the prompt mentions a seat id that is not in visible_ids.
    Seat ids are the integers 0 .. n_seats-1. A mention is the substring f"seat {j}".
    """
    raise NotImplementedError("T2-b crux: fill prompt_is_ok")


if __name__ == "__main__":
    visible = {0: 1.0, 1: 0.0}
    text = prompt_for(0, visible, ["seat 1: hello"])
    print(text)
    print("---")
    ok, reason = prompt_is_ok(text, set(visible), n_seats=4)
    print("ok", ok, reason)
