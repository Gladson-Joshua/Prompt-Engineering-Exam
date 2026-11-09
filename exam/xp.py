"""Live XP / streak rules applied while answering (mirrors setAnswer in the HTML)."""
from __future__ import annotations

from .grading import SECTION_BY_ID, is_answered, questions_of
from .models import Question


def apply_answer(state: dict, q: Question, value) -> list[str]:
    """Store an answer, update XP/streak/cleared levels. Returns toast messages."""
    toasts: list[str] = []
    answers = state["answers"]
    was = is_answered(q, answers.get(q.n))
    answers[q.n] = value
    now = is_answered(q, value)

    if not was and now:
        state["xp"] += 10
        if q.type != "keywords":
            state["streak"] += 1
            if state["streak"] % 5 == 0:
                state["xp"] += 10
                toasts.append(f"{state['streak']} in a row · +10 XP")
    elif was and not now:
        state["streak"] = 0
        state["xp"] = max(0, state["xp"] - 10)

    if q.sec not in state["cleared_sections"] and all(
        is_answered(x, answers.get(x.n)) for x in questions_of(q.sec)
    ):
        state["cleared_sections"].append(q.sec)
        state["xp"] += 25
        toasts.append(f"Level {SECTION_BY_ID[q.sec].level} cleared · +25 XP")
    return toasts
