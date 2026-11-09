"""Scoring logic, ported 1:1 from the HTML exam. No Streamlit imports here."""
from __future__ import annotations

import math
from datetime import datetime, timezone

from .data import BADGES, LEVELS, QUESTIONS, ROASTS, SECTIONS
from .models import Question

SECTION_BY_ID = {s.id: s for s in SECTIONS}
GRADED = [q for q in QUESTIONS if q.type != "keywords"]
KEYWORD_Q = next(q for q in QUESTIONS if q.type == "keywords")
SCORED_SECTIONS = [s for s in SECTIONS if s.marks]


def questions_of(sec_id: str) -> list[Question]:
    return [q for q in QUESTIONS if q.sec == sec_id]


def round1(x: float) -> float:
    """JavaScript Math.round(x*10)/10 (halves round up, not to even)."""
    return math.floor(x * 10 + 0.5) / 10


def word_count(text: str | None) -> int:
    return len((text or "").split())


def is_answered(q: Question, answer) -> bool:
    if q.type == "mcq":
        return isinstance(answer, int) and not isinstance(answer, bool)
    if q.type == "keywords":
        return isinstance(answer, list) and any(x and x.strip() for x in answer)
    return isinstance(answer, str) and answer.strip() != ""


def answered_count(answers: dict) -> int:
    return sum(is_answered(q, answers.get(q.n)) for q in GRADED)


def keyword_count(answers: dict) -> int:
    kw = answers.get(KEYWORD_Q.n)
    return sum(1 for x in kw if x and x.strip()) if isinstance(kw, list) else 0


def score_text(answer: str | None, q: Question) -> dict:
    text = (answer or "").strip()
    words = word_count(text)
    if not text or (q.min_words and words < math.ceil(q.min_words * 0.5)):
        return {"score": 0, "hits": [{"label": r.label, "hit": False} for r in q.rubric], "short": True}

    score, hits = 0.0, []
    for r in q.rubric:
        if r.count:
            matches = [m.group(0) for m in r.pattern.finditer(text)]
            if r.distinct:
                n = len({m.lower()[:-1] if m.lower().endswith("s") else m.lower() for m in matches})
            else:
                n = len(matches)
            score += min(r.cap, n) * r.each
            hits.append({"label": f"{r.label} ({min(r.cap, n)} found)", "hit": n > 0})
        else:
            ok = r.pattern.search(text) is not None
            if ok:
                score += r.pts
            hits.append({"label": r.label, "hit": ok})

    short = bool(q.min_words and words < q.min_words)
    if short:
        score *= 0.8  # thin-answer penalty
    return {"score": min(q.marks, round1(score)), "hits": hits, "short": short}


def _letter(total: float) -> str:
    for cut, g in ((90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D")):
        if total >= cut:
            return g
    return "F"


def grade(state: dict) -> dict:
    """state: user, answers, started_at, finished_at (epoch seconds), cleared_sections."""
    answers = state["answers"]
    per_q, detail = {}, {}
    sections = {s.id: 0.0 for s in SCORED_SECTIONS}
    for q in GRADED:
        a = answers.get(q.n)
        if q.type == "mcq":
            ok = a == q.ans and is_answered(q, a)
            per_q[q.n] = 1 if ok else 0
            detail[q.n] = {"ok": ok, "chosen": a}
        else:
            r = score_text(a, q)
            per_q[q.n] = r["score"]
            detail[q.n] = r
        sections[q.sec] += per_q[q.n]

    sections = {k: round1(v) for k, v in sections.items()}
    total = round1(sum(sections.values()))
    kw = keyword_count(answers)
    minutes = max(0.0, (state["finished_at"] - state["started_at"]) / 60)
    answered = answered_count(answers)
    base = {"total": total, "sections": sections, "per_q": per_q, "keywords": kw,
            "minutes": minutes, "answered": answered}

    badges = []
    for b in BADGES:
        try:
            if b.test(base):
                badges.append(b.id)
        except Exception:
            pass

    xp = (round(total * 10) + answered * 10 + kw * 10 + len(badges) * 50
          + len(state.get("cleared_sections", [])) * 25)
    level = next(l for l in reversed(LEVELS) if xp >= l.xp)
    tier = next((r for r in ROASTS if total <= r.max), ROASTS[-1])
    h = sum(ord(ch) for ch in state["user"]["name"])  # same seed as the HTML (UTF-16 units for BMP text)
    roast = tier.lines[h % len(tier.lines)]

    return {**base, "detail": detail, "badges": badges, "xp": xp, "level": level.name,
            "grade": _letter(total), "roast": roast, "roast_tag": tier.tag,
            "date": datetime.fromtimestamp(state["finished_at"], tz=timezone.utc).isoformat()}


def fmt(n: float) -> str:
    return str(int(n)) if float(n).is_integer() else f"{n:.1f}"
