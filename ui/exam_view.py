"""Exam screen: sidebar of levels + timer, one question card at a time."""
from __future__ import annotations

import time

import streamlit as st

from exam.data import EXAM_MINUTES, QUESTIONS, SECTIONS
from exam.grading import GRADED, SECTION_BY_ID, answered_count, is_answered, questions_of, word_count
from exam.xp import apply_answer

from .state import S, finish_exam, persist, toast
from .theme import brand_html, e, html

LETTERS = "ABCD"


# ---------- state mutations (widget callbacks) ----------
def _go(i: int) -> None:
    S()["idx"] = max(0, min(len(QUESTIONS) - 1, i))
    persist()


def _on_mcq(q) -> None:
    label = st.session_state[f"q{q.n}"]
    _commit(q, q.opts.index(label.split(" · ", 1)[1]) if label else None)


def _on_text(q) -> None:
    _commit(q, st.session_state[f"q{q.n}"])


def _on_keyword(q) -> None:
    _commit(q, [st.session_state.get(f"kw{i}", "") for i in range(10)])


def _commit(q, value) -> None:
    for m in apply_answer(S(), q, value):
        toast(m)
    persist()


# ---------- sidebar ----------
def _time_left() -> float:
    return max(0.0, EXAM_MINUTES * 60 - (time.time() - S()["started_at"]))


@st.fragment(run_every=1)
def _timer() -> None:
    s = S()
    if s.get("result"):
        return
    left = _time_left()
    m, sec = divmod(int(left), 60)
    low = " low" if left < 5 * 60 else ""
    html(f'<div class="timer num{low}">⏱ {m:02d}:{sec:02d}</div>')
    if left <= 0:
        st.toast("Time is up — submitting your answers")
        finish_exam()
        st.rerun(scope="app")


def _sidebar() -> None:
    s, answers = S(), S()["answers"]
    cur_sec = QUESTIONS[s["idx"]].sec
    with st.sidebar:
        html(brand_html())
        u = s["user"]
        html(f'<div class="candidate"><b>{e(u["name"])}</b><span>{e(u["email"])}</span><span>{e(u["batch"])}</span></div>')
        st.write("")
        _timer()
        n = answered_count(answers)
        st.progress(n / len(GRADED), text=f"{n} of {len(GRADED)} answered · {round(n / len(GRADED) * 100)}%")
        html(f'<div class="chips"><div class="chip xp"><b class="num">{s["xp"]}</b>XP</div>'
             f'<div class="chip streak"><b class="num">{s["streak"]}</b>Streak</div></div>')
        st.write("")
        html('<div class="eyebrow">Levels</div>')
        for sec in SECTIONS:
            qs = questions_of(sec.id)
            done = sum(is_answered(q, answers.get(q.n)) for q in qs)
            tick = " ✓" if done == len(qs) else ""
            first = next(i for i, q in enumerate(QUESTIONS) if q.sec == sec.id)
            st.button(f"L{sec.level} · {sec.name}  ({done}/{len(qs)}){tick}", key=f"lvl{sec.id}",
                      type="primary" if sec.id == cur_sec else "secondary", use_container_width=True,
                      on_click=_go, args=(first,), help=sec.sub)
        st.write("")
        if st.button("Finish exam", use_container_width=True, icon=":material/flag:"):
            _confirm_finish()


@st.dialog("Submit your exam?")
def _confirm_finish() -> None:
    left = len(GRADED) - answered_count(S()["answers"])
    if left:
        st.write(f"**{left}** question{'s are' if left > 1 else ' is'} still unanswered. "
                 "Unanswered questions score zero. Submit anyway?")
    else:
        st.write(f"All {len(GRADED)} questions answered. Submit to see your score, rank and roast.")
    c1, c2 = st.columns(2)
    if c1.button("Keep working", use_container_width=True):
        st.rerun()
    if c2.button("Submit", type="primary", use_container_width=True):
        finish_exam()
        st.rerun()


# ---------- question card ----------
def _dots(q) -> None:
    qs = questions_of(q.sec)
    answers = S()["answers"]
    per_row = 10
    for start in range(0, len(qs), per_row):
        cols = st.columns(per_row, gap="small")
        for col, x in zip(cols, qs[start:start + per_row]):
            ans = is_answered(x, answers.get(x.n))
            key = f"dot{'ans' if ans else ''}_{x.n}"
            idx = QUESTIONS.index(x)
            col.button("★" if x.type == "keywords" else str(x.n), key=key, use_container_width=True,
                       type="primary" if x.n == q.n else "secondary", on_click=_go, args=(idx,))


def _body(q) -> None:
    a = S()["answers"].get(q.n)
    if q.type == "mcq":
        labels = [f"{LETTERS[i]} · {o}" for i, o in enumerate(q.opts)]
        st.radio("Choose one", labels, index=a if isinstance(a, int) else None, key=f"q{q.n}",
                 label_visibility="collapsed", on_change=_on_mcq, args=(q,))
    elif q.type == "keywords":
        arr = a if isinstance(a, list) else [""] * 10
        cols = st.columns(2)
        for i in range(10):
            cols[i % 2].text_input(f"{i + 1}.", value=arr[i] if i < len(arr) else "", key=f"kw{i}",
                                   placeholder="e.g. Analyze deeply", on_change=_on_keyword, args=(q,))
    else:
        is_prompt = q.type == "prompt"
        ph = ("Write the prompt exactly as you would paste it into ChatGPT, Claude or Gemini…"
              if is_prompt else "Write your answer here…")
        st.text_area("Your answer", value=a or "", key=f"q{q.n}", height=260 if is_prompt else 150,
                     placeholder=ph, label_visibility="collapsed", on_change=_on_text, args=(q,))
        words = word_count(a)
        aim = f"Aim for {q.min_words}+ words · " if q.min_words else ""
        st.caption(f"{aim}{words} words saved · answers save when you click outside the box or press Ctrl+Enter")


def render() -> None:
    s = S()
    if _time_left() <= 0:
        finish_exam()
        st.rerun()
    _sidebar()
    q = QUESTIONS[s["idx"]]
    sec = SECTION_BY_ID[q.sec]
    _dots(q)
    with st.container(border=True):
        marks = f"{q.marks} mark{'s' if q.marks > 1 else ''}" if q.marks else "XP only"
        num = "Bonus" if q.type == "keywords" else f"Question {q.n} of {len(GRADED)}"
        html(f'<div class="qhead"><span class="pill">L{sec.level} · {e(sec.name)}</span>'
             f'<span class="qn">{num}</span><span class="marks">{marks}</span></div>'
             f'<div class="qtext">{e(q.q)}</div>'
             + (f'<div class="quote">{e(q.quote)}</div>' if q.quote else "")
             + (f'<div class="hint">💡 {e(q.hint)}</div>' if q.hint else ""))
        _body(q)
        c1, _, c3 = st.columns([1, 2, 1])
        c1.button("← Previous", disabled=s["idx"] == 0, use_container_width=True, on_click=_go, args=(s["idx"] - 1,))
        if s["idx"] == len(QUESTIONS) - 1:
            if c3.button("Finish exam", type="primary", use_container_width=True):
                _confirm_finish()
        else:
            c3.button("Next →", type="primary", use_container_width=True, on_click=_go, args=(s["idx"] + 1,))
