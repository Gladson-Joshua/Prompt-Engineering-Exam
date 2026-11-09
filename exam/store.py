"""Server-side persistence: one JSON file per candidate email (replaces browser localStorage).

Files are named by a hash of the email so the attempt key can sit in the page URL
(?attempt=...) without exposing the address, and a browser refresh can resume.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "attempts"
_KEY_RE = re.compile(r"^[0-9a-f]{24}$")


def key_for(email: str) -> str:
    return hashlib.sha256(email.strip().lower().encode()).hexdigest()[:24]


def _path(key: str) -> Path:
    return DATA_DIR / f"{key}.json"


def save(state: dict) -> None:
    if not state.get("user"):
        return
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data = {**state, "answers": {str(k): v for k, v in state["answers"].items()}}
    if data.get("result"):
        r = data["result"]
        data["result"] = {**r, "per_q": {str(k): v for k, v in r["per_q"].items()},
                          "detail": {str(k): v for k, v in r["detail"].items()}}
    target = _path(key_for(state["user"]["email"]))
    tmp = target.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(target)


def load_key(key: str) -> dict | None:
    if not _KEY_RE.match(key or ""):
        return None
    p = _path(key)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    data["answers"] = {int(k): v for k, v in data.get("answers", {}).items()}
    if data.get("result"):
        r = data["result"]
        r["per_q"] = {int(k): v for k, v in r["per_q"].items()}
        r["detail"] = {int(k): v for k, v in r["detail"].items()}
    return data


def load(email: str) -> dict | None:
    return load_key(key_for(email))


def clear(email: str) -> None:
    _path(key_for(email)).unlink(missing_ok=True)
