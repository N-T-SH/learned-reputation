"""Recover a seat reply that is almost JSON.

Fireworks replies often truncate, wrap the object in prose, or put nominate
in a string. OpenRouter replies were already objects. This does not invent
a contribution or a nomination that was not written.
"""

from __future__ import annotations

import json
import re


def _close(fragment: str) -> str:
    text = fragment.rstrip().rstrip(",")
    if text.count("\"") % 2:
        text += "\""
    opens = text.count("[") - text.count("]")
    braces = text.count("{") - text.count("}")
    text += "]" * max(opens, 0)
    text += "}" * max(braces, 0)
    return text


def parse_reply(text: str):
    raw = (text or "").strip()
    raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?", "", raw).strip()
        raw = re.sub(r"```$", "", raw).strip()
    start = raw.find("{")
    if start < 0:
        return text
    chunk = raw[start:]
    end = chunk.rfind("}")
    candidates = [chunk if end < 0 else chunk[: end + 1], _close(chunk)]
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return text


def _checks() -> None:
    cases = [
        ('{"message": "hi", "nominate": ["aa"], "contribute": 1}', ["aa"], 1.0),
        ('prose {"message": "hi", "nominate": null, "contribute": 0.5}', [], 0.5),
        ('{"message": "hi", "nominate": "bb", "contribute": "0.3"}', ["bb"], 0.3),
        ('{"nominate": ["cc"], "contribute": 1', ["cc"], 1.0),
        ('<think>x</think>{"message": "", "nominate": false, "contribute": 0}', [], 0.0),
    ]
    from envs.pgg_scripted.schema import repair

    for text, noms, contrib in cases:
        action, ok = repair(parse_reply(text), ["aa", "bb", "cc"])
        if not ok or action["nominate"] != noms or action["contribute"] != contrib:
            raise SystemExit(f"parse failed on {text!r} -> {action} ok={ok}")
    print("parse_ok", len(cases))


if __name__ == "__main__":
    _checks()
