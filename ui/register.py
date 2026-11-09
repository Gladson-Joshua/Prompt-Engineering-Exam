"""Registration screen."""
from __future__ import annotations

import re

import streamlit as st

from exam import store
from exam.data import EXAM_MINUTES, SECTIONS, TOTAL_MARKS
from exam.grading import GRADED

from .state import begin, new_state
from .theme import brand_html, e, html

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")
BATCHES = [f"Batch {i}" for i in range(1, 16)]


def _hero() -> None:
    track = "".join(
        f'<div class="row"><span class="dot">L{s.level}</span><span>{e(s.name)}'
        f'<span class="muted"> · {e(s.sub.split("·")[0].strip())}</span></span>'
        f'<span class="m">{f"{s.marks} marks" if s.marks else "XP"}</span></div>'
        for s in SECTIONS)
    html(f"""<div class="hero">{brand_html()}
      <div class="eyebrow" style="margin-top:14px">Written practice · Level assessment</div>
      <h1>Prompt Engineering Exam</h1>
      <p>Five levels covering RTCFR, prompt chaining, CoT, ToT, ReAct, multi-agent prompting, prompt injection and
      reverse prompting. Clear each level to earn XP, collect badges, and find out your rank at Social Eagle.</p>
      <div class="stats">
        <div class="stat"><b class="num">{len(GRADED)}</b><span>Questions</span></div>
        <div class="stat"><b class="num">{TOTAL_MARKS}</b><span>Marks</span></div>
        <div class="stat"><b class="num">{EXAM_MINUTES}</b><span>Minutes</span></div>
      </div>
      <div class="track">{track}</div></div>""")


def _resume_choice(saved: dict) -> None:
    name = saved["user"]["name"]
    if saved.get("result"):
        st.info(f"A finished attempt exists for this email ({name}).")
        label = "View last result"
    else:
        st.info(f"An unfinished attempt exists for this email ({name}). The timer kept running since it started.")
        label = "Resume attempt"
    c1, c2 = st.columns(2)
    if c1.button(label, type="primary", use_container_width=True):
        st.session_state.pop("_pending", None)
        begin(saved)
        st.rerun()
    if c2.button("Start a new attempt", use_container_width=True):
        user = st.session_state.pop("_pending")["user_new"]
        store.clear(user["email"])
        begin(new_state(user))
        st.rerun()


def render() -> None:
    left, right = st.columns([1.15, 1], gap="large")
    with left:
        _hero()
    with right:
        html('<div class="eyebrow">Register to enter</div>')
        st.subheader("Who's taking the test?")
        pending = st.session_state.get("_pending")
        if pending:
            _resume_choice(pending["saved"])
            if st.button("← Back", type="tertiary"):
                st.session_state.pop("_pending")
                st.rerun()
            return

        with st.form("register", border=False):
            name = st.text_input("Full name", placeholder="e.g. Priya Raman", autocomplete="name")
            email = st.text_input("Email", placeholder="you@example.com", autocomplete="email")
            batch = st.selectbox("Batch / Class", BATCHES, index=None, placeholder="Select your batch")
            st.caption(f"The {EXAM_MINUTES}-minute timer starts when you enter.")
            submitted = st.form_submit_button("Enter the exam →", type="primary", use_container_width=True)

        if submitted:
            name, email = name.strip(), email.strip()
            errs = []
            if len(name) < 2:
                errs.append("Enter your full name.")
            if not EMAIL_RE.match(email):
                errs.append("Enter a valid email address.")
            if not batch:
                errs.append("Select your batch.")
            if errs:
                for m in errs:
                    st.error(m)
                return
            user = {"name": name, "email": email, "batch": batch}
            saved = store.load(email)
            if saved:
                st.session_state["_pending"] = {"saved": saved, "user_new": user}
                st.rerun()
            begin(new_state(user))
            st.rerun()

        st.caption("Your answers are saved on the exam server as you go, so you can resume after a refresh. "
                   "Avoid entering sensitive personal information.")
