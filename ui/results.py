"""Results screen: score ring, roast, level breakdown, badges, actions, answer review."""
from __future__ import annotations

import re
from datetime import datetime

import streamlit as st

from exam.data import BADGES, LEVELS, SECTION_NOTES
from exam.grading import GRADED, SCORED_SECTIONS, fmt, questions_of
from exam.pdf import build_scorecard

from .state import S, retake
from .theme import brand_html, e, html

LETTERS = "ABCD"
ICONS = {
    "rookie": '<path d="M12 3l2.5 5 5.5.8-4 3.9.9 5.5L12 15.6 7.1 18.2l.9-5.5-4-3.9L9.5 8z"/>',
    "smith": '<path d="M14 4l6 6-9 9H5v-6z"/><path d="M12 6l6 6"/>',
    "chain": '<path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/>',
    "shield": '<path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z"/><path d="M9 12l2 2 4-4"/>',
    "vault": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M12 9v-2M12 17v-2"/>',
    "speed": '<path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/>',
    "clear": '<path d="M20 6L9 17l-5-5"/>',
    "legend": '<path d="M6 3h12v4a6 6 0 0 1-12 0z"/><path d="M6 5H3a3 3 0 0 0 3 4M18 5h3a3 3 0 0 1-3 4M12 13v4M8 21h8M9 17h6"/>',
}
BADGE_COL = {"rookie": "var(--accent)", "smith": "var(--teal)", "chain": "var(--purple)", "shield": "var(--good)",
             "vault": "var(--xp)", "speed": "var(--coral)", "clear": "var(--accent)", "legend": "var(--purple)"}


def summary_text(user: dict, r: dict) -> str:
    lines = [f"Social Eagle · Prompt Engineering Exam", f"{user['name']} · {user['batch']}",
             f"Score: {fmt(r['total'])}/100 (Grade {r['grade']}) · Rank: {r['level']} · {r['xp']} XP"]
    lines += [f"L{s.level} {s.name}: {fmt(r['sections'][s.id])}/{s.marks}" for s in SCORED_SECTIONS]
    names = [b.name for b in BADGES if b.id in r["badges"]]
    lines += [f"Badges: {', '.join(names) or 'none'}", f"Roast: {r['roast']}"]
    return "\n".join(lines)


def _hero(user: dict, r: dict) -> None:
    lvl_idx = next(i for i, l in enumerate(LEVELS) if l.name == r["level"])
    nxt = next((l for l in LEVELS if l.xp > r["xp"]), None)
    lvl_pct = round((r["xp"] - LEVELS[lvl_idx].xp) / (nxt.xp - LEVELS[lvl_idx].xp) * 100) if nxt else 100
    mins = int(r["minutes"]); secs = round((r["minutes"] - mins) * 60)
    date = datetime.fromisoformat(r["date"]).astimezone().strftime("%d %b %Y")
    circ = 439.8  # 2πr for r=70
    off = circ - circ * min(1, r["total"] / 100)
    to_next = f"{nxt.xp - r['xp']} XP to {e(nxt.name)}" if nxt else "Max rank reached"
    html(f"""<div class="res-hero">
      <div class="ring"><svg viewBox="0 0 160 160"><circle class="trk" cx="80" cy="80" r="70"/>
        <circle class="bar" cx="80" cy="80" r="70" stroke-dasharray="{circ}" stroke-dashoffset="{off:.1f}"/></svg>
        <div class="lbl"><div><b class="num">{fmt(r['total'])}</b><span>out of 100</span></div></div></div>
      <div class="res-meta">
        <div class="eyebrow">Exam complete · {e(user['batch'])}</div>
        <h2>{e(user['name'])}, you rank <span style="color:var(--accent)">{e(r['level'])}</span></h2>
        <div><span class="grade-pill">Grade {r['grade']}</span><span class="muted">{len(r['badges'])} of {len(BADGES)} badges</span></div>
        <div class="kv"><span>Time <b class="num">{mins}m {secs}s</b></span><span>Answered <b class="num">{r['answered']}/{len(GRADED)}</b></span>
          <span>Keywords <b class="num">{r['keywords']}/10</b></span><span>Date <b>{date}</b></span></div>
        <div class="plabel"><span><b class="num">{r['xp']} XP</b> · {e(r['level'])}</span><span class="muted">{to_next}</span></div>
        <div class="bar-outer xp"><i style="width:{lvl_pct}%"></i></div>
      </div></div>""")
    html(f"""<div class="roast"><div class="flame"><svg viewBox="0 0 24 24"><path d="M12 2c1 4 6 6 6 12a6 6 0 0 1-12 0c0-3 2-5 2-7 1 1.5 2 2.5 3 2.5s1-4.5 1-7.5z"/></svg></div>
      <div><div class="eyebrow" style="color:var(--coral)">The roast · {e(r['roast_tag'])}</div>
      <blockquote>“{e(r['roast'])}”</blockquote><div class="tag">Served at {fmt(r['total'])}/100. Retake to change the verdict.</div></div></div>""")


def _panels(r: dict) -> None:
    rows, notes = "", ""
    for s in SCORED_SECTIONS:
        got = r["sections"][s.id]; p = got / s.marks
        rows += (f'<div class="secrow"><div class="top"><span>L{s.level} · {e(s.name)}<small>{e(s.sub)}</small></span>'
                 f'<b class="num">{fmt(got)} / {s.marks}</b></div><div class="bar-outer"><i style="width:{round(p * 100)}%"></i></div></div>')
        good = p >= 0.7
        notes += (f'<div><span class="{"ok" if good else "no"}">{"✓" if good else "!"}</span>'
                  f'<span>{e(SECTION_NOTES[s.id]["good" if good else "weak"])}</span></div>')
    badges = "".join(
        f'<div class="badge {"" if b.id in r["badges"] else "locked"}"><span class="ic" style="background:{BADGE_COL[b.id]}">'
        f'<svg viewBox="0 0 24 24">{ICONS[b.id]}</svg></span><span><b>{e(b.name)}</b><span>{e(b.desc)}</span></span></div>'
        for b in BADGES)
    c1, c2 = st.columns(2)
    with c1:
        html(f'<div class="panel"><h3>Level breakdown</h3>{rows}<div class="notes">{notes}</div></div>')
    with c2:
        html(f'<div class="panel"><h3>Badges</h3><div class="badges">{badges}</div></div>')


def _actions(user: dict, r: dict) -> None:
    st.write("")
    c1, c2, c3 = st.columns([1.4, 1, 1])
    fname = "SocialEagle_Scorecard_" + re.sub(r"[^a-z0-9]+", "_", user["name"], flags=re.I) + ".pdf"
    c1.download_button("Download scorecard (PDF)", data=build_scorecard(user, r), file_name=fname,
                       mime="application/pdf", type="primary", use_container_width=True, icon=":material/download:")
    with c2.popover("Copy summary", use_container_width=True, icon=":material/content_copy:"):
        st.caption("Use the copy icon in the top-right corner of the box.")
        st.code(summary_text(user, r), language=None)
    if c3.button("Retake exam", use_container_width=True, icon=":material/restart_alt:"):
        _confirm_retake()


@st.dialog("Retake the exam?")
def _confirm_retake() -> None:
    st.write("This deletes your saved result and answers, then returns to registration.")
    c1, c2 = st.columns(2)
    if c1.button("Cancel", use_container_width=True):
        st.rerun()
    if c2.button("Retake", type="primary", use_container_width=True):
        retake()
        st.rerun()


def _review(r: dict) -> None:
    answers = S()["answers"]
    st.subheader("Answer review")
    st.caption("Written answers are rubric-graded. Green chips are the criteria your answer hit.")
    for s in SCORED_SECTIONS:
        st.markdown(f"#### L{s.level} · {s.name} — {fmt(r['sections'][s.id])} / {s.marks}")
        for q in questions_of(s.id):
            sc, d = r["per_q"][q.n], r["detail"][q.n]
            mark = "🟢" if sc >= q.marks else "🟡" if sc > 0 else "🔴"
            with st.expander(f"{mark} Q{q.n} · {q.q} — {fmt(sc)}/{q.marks}"):
                if q.quote:
                    html(f'<div class="quote">{e(q.quote)}</div>')
                if q.type == "mcq":
                    ch = d["chosen"]
                    st.markdown(f"Your answer: **{LETTERS[ch]}** · {q.opts[ch]}" if isinstance(ch, int) else "Not answered")
                    st.markdown(f"Correct: **{LETTERS[q.ans]}** · {q.opts[q.ans]}")
                else:
                    a = answers.get(q.n)
                    chips = "".join(f'<span class="{"hit" if h["hit"] else "miss"}">{"✓" if h["hit"] else "✗"} {e(h["label"])}</span>'
                                    for h in d["hits"])
                    html(f'<div class="yours">{e(a) if a else "— not answered —"}</div><div class="crit">{chips}</div>')
                    if d.get("short"):
                        st.caption("Short answer — thin-answer penalty applied.")


def render() -> None:
    s = S()
    user, r = s["user"], s["result"]
    if st.session_state.pop("_celebrate", False):
        st.balloons()
    html(brand_html())
    _hero(user, r)
    _panels(r)
    _actions(user, r)
    st.divider()
    _review(r)
