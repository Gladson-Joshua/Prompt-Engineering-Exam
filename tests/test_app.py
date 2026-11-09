import shutil

import pytest
from streamlit.testing.v1 import AppTest

from exam import store
from exam.data import QUESTIONS
from exam.grading import grade
from exam.pdf import build_scorecard


@pytest.fixture(autouse=True)
def tmp_store(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "DATA_DIR", tmp_path / "attempts")


def _register(at, email="priya@example.com"):
    at.text_input[0].input("Priya Raman")
    at.text_input[1].input(email)
    at.selectbox[0].select("Batch 3")
    at.button[0].click().run()


def test_full_flow():
    at = AppTest.from_file("../app.py", default_timeout=30).run()
    assert not at.exception
    _register(at)
    assert not at.exception
    S = at.session_state.S
    assert S["user"]["batch"] == "Batch 3"
    # answer Q1 correctly
    at.radio(key="q1").set_value(at.radio(key="q1").options[0]).run()
    assert at.session_state.S["answers"][1] == 0
    assert at.session_state.S["xp"] == 10
    # go next, answer nothing, then jump to last question via level button and submit
    at.button(key="lvlE").click().run()
    at.text_input(key="kw0").input("Analyze deeply").run()
    assert at.session_state.S["answers"][51][0] == "Analyze deeply"
    # simulate submit directly (dialogs are not drivable in AppTest)
    s = at.session_state.S
    import time
    s["finished_at"] = time.time(); s["result"] = grade(s)
    at.run()
    assert not at.exception
    assert any("you rank" in m.value for m in at.markdown)
    assert store.load("priya@example.com")["user"]["name"] == "Priya Raman"


def test_text_answer_and_resume():
    at = AppTest.from_file("../app.py", default_timeout=30).run()
    _register(at, "r@example.com")
    at.button(key="lvlC").click().run()
    q = next(q for q in QUESTIONS if q.sec == "C")
    at.text_area(key=f"q{q.n}").input("Act as a senior strategist and think step by step about the plan").run()
    assert not at.exception
    saved = store.load("r@example.com")
    assert saved["answers"][q.n].startswith("Act as")
    # new session resumes from the URL key
    at2 = AppTest.from_file("../app.py", default_timeout=30)
    at2.query_params["attempt"] = store.key_for("r@example.com")
    at2.run()
    assert not at2.exception
    assert at2.session_state.S["answers"][q.n].startswith("Act as")


def test_pdf_builds():
    s = {"user": {"name": "Priya “P” Raman", "email": "p@x.com", "batch": "Batch 1"},
         "answers": {q.n: q.ans for q in QUESTIONS if q.type == "mcq"}, "started_at": 0, "finished_at": 1800,
         "cleared_sections": ["A"]}
    pdf = build_scorecard(s["user"], grade(s))
    assert pdf[:4] == b"%PDF" and len(pdf) > 5000
