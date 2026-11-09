"""Session-state helpers shared by the screens."""
from __future__ import annotations

import time

import streamlit as st

from exam import store
from exam.grading import grade


def new_state(user: dict | None = None) -> dict:
    return {"user": user, "answers": {}, "started_at": time.time() if user else None, "finished_at": None,
            "idx": 0, "xp": 0, "streak": 0, "cleared_sections": [], "result": None}


def S() -> dict:
    if "S" not in st.session_state:
        st.session_state.S = new_state()
    return st.session_state.S


def persist() -> None:
    store.save(S())


def toast(msg: str) -> None:
    st.session_state.setdefault("_toasts", []).append(msg)


def flush_toasts() -> None:
    for m in st.session_state.pop("_toasts", []):
        st.toast(m)


def begin(state: dict) -> None:
    st.session_state.S = state
    st.query_params["attempt"] = store.key_for(state["user"]["email"])
    persist()


def finish_exam() -> None:
    s = S()
    if s.get("result"):
        return
    s["finished_at"] = time.time()
    s["result"] = grade(s)
    st.session_state["_celebrate"] = True
    persist()


def retake() -> None:
    s = S()
    if s.get("user"):
        store.clear(s["user"]["email"])
    st.session_state.clear()
    st.query_params.clear()
