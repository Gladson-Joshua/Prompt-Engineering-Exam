import json
from pathlib import Path

import pytest

from exam.data import QUESTIONS
from exam.grading import GRADED, answered_count, grade, score_text
from exam.xp import apply_answer

Q = {q.n: q for q in QUESTIONS}
CASES = json.loads((Path(__file__).parent / "fixtures" / "js_expected.json").read_text(encoding="utf-8"))


def test_question_bank_shape():
    assert len(QUESTIONS) == 51
    assert len(GRADED) == 50
    assert sum(q.marks for q in GRADED) == 90


@pytest.mark.parametrize("case", CASES, ids=lambda c: f"Q{c['n']}")
def test_score_text_matches_javascript(case):
    r = score_text(case["answer"], Q[case["n"]])
    assert r["score"] == pytest.approx(case["score"])
    assert [[h["label"], h["hit"]] for h in r["hits"]] == case["hits"]
    assert bool(r["short"]) == case["short"]


def _state(**kw):
    return {"user": {"name": "Priya Raman", "email": "p@x.com", "batch": "Batch 1"},
            "answers": {}, "started_at": 0, "finished_at": 30 * 60, "xp": 0, "streak": 0,
            "cleared_sections": [], **kw}


def test_perfect_mcq_section():
    s = _state(answers={q.n: q.ans for q in QUESTIONS if q.type == "mcq"})
    r = grade(s)
    assert r["sections"]["A"] == 20
    assert "rookie" in r["badges"]


def test_xp_streak_and_level_clear():
    s = _state()
    msgs = []
    for q in [q for q in QUESTIONS if q.sec == "A"]:
        msgs += apply_answer(s, q, 0)
    # 20 answers * 10 + 4 streak bonuses * 10 + level clear 25
    assert s["xp"] == 200 + 40 + 25
    assert "A" in s["cleared_sections"]
    assert any("cleared" in m for m in msgs)
    apply_answer(s, Q[1], None)
    assert s["streak"] == 0 and answered_count(s["answers"]) == 19
