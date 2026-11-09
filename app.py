"""Social Eagle Prompt Engineering Exam — Streamlit edition.

Run:  streamlit run app.py
"""
from pathlib import Path

import streamlit as st

from exam import store
from ui import exam_view, register, results
from ui.state import S, flush_toasts
from ui.theme import inject

st.set_page_config(page_title="Social Eagle Prompt Exam",
                   page_icon=str(Path(__file__).parent / "assets" / "logo.png"), layout="wide")
inject()

# Resume after a browser refresh: the attempt key lives in the URL.
if "S" not in st.session_state and (key := st.query_params.get("attempt")):
    saved = store.load_key(key)
    if saved:
        st.session_state.S = saved
    else:
        st.query_params.clear()

state = S()
flush_toasts()
if not state.get("user"):
    register.render()
elif state.get("result"):
    results.render()
else:
    exam_view.render()
