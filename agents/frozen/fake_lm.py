"""Stand-in speaker. Not a model result.

Returns a JSON string so the rest of the loop matches a real model:
prompt in, text out, then parse, then repair.
"""

from __future__ import annotations

import json


def complete(seat: int, prompt: str) -> str:
    raw = {
        "message": f"seat {seat} speaking",
        "nominate": [seat, 0],
        "contribute": 1.0,
    }
    return json.dumps(raw)
