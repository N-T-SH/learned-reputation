"""OpenRouter speaker. Returns text, never a dict.

The key stays in the environment. Model may be passed in; otherwise
OPENROUTER_MODEL is the fallback.

reasoning_off sends enabled false. gpt-oss-20b on OpenRouter rejects this
(reasoning is mandatory there). Qwen accepts a disable. A reject still errors.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

BASE = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openrouter/free"


def complete(seat: int, prompt: str, model: str | None = None, reasoning_off: bool = True) -> str:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is not set. FakeLM is the no-key path.")
    chosen = (model or os.environ.get("OPENROUTER_MODEL") or DEFAULT_MODEL).strip()
    body = {
        "model": chosen,
        "temperature": 0,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Reply with one JSON object only. Keys: message (string), "
                    "nominate (list of integers), contribute (number from 0 to 1). "
                    "No markdown."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    }
    if reasoning_off:
        body["reasoning"] = {"enabled": False}
    req = urllib.request.Request(
        BASE,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode()[:300]
        raise RuntimeError(f"OpenRouter HTTP {exc.code}: {detail}") from exc
    return payload["choices"][0]["message"]["content"]
