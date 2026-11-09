"""Social Eagle look for Streamlit: CSS tokens, fonts and small HTML helpers."""
from __future__ import annotations

import base64
from functools import lru_cache
from html import escape
from pathlib import Path

import streamlit as st

LOGO = Path(__file__).resolve().parent.parent / "assets" / "logo.png"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Figtree:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root{
  --bg:#f7f4f4; --surface:#ffffff; --surface-2:#f1eaeb; --fg:#1a1a1a; --muted:#6b6468; --line:#e4dadc;
  --accent:#b5202f; --accent-2:#8e1a24; --accent-soft:#fbeaec; --accent-line:#efb6bd;
  --good:#15803d; --good-soft:#dcfce7; --warn:#b45309; --warn-soft:#fef3c7; --bad:#b91c1c; --bad-soft:#fee2e2;
  --xp:#d97706; --xp-soft:#fff1d6; --teal:#0f9b8e; --purple:#7c3aed; --coral:#e0434f;
  --display:'Sora',ui-sans-serif,system-ui,'Segoe UI',sans-serif;
  --body:'Figtree',ui-sans-serif,system-ui,'Segoe UI',sans-serif;
}
html, body, [data-testid="stAppViewContainer"], .stMarkdown, .stTextArea textarea, .stTextInput input, button, label { font-family: var(--body); }
h1, h2, h3, h4 { font-family: var(--display) !important; letter-spacing: -.01em; }
[data-testid="stSidebar"] { background: var(--surface); border-right: 1px solid var(--line); }
.block-container { padding-top: 2rem; max-width: 980px; }
.num { font-variant-numeric: tabular-nums; }
.eyebrow { font-family: var(--display); font-size: 11px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--accent); }
.muted { color: var(--muted); }

.brand { display:flex; align-items:center; gap:10px; margin-bottom:6px; }
.brand img { width:40px; height:40px; border-radius:10px; }
.brand b { font-family:var(--display); font-weight:800; letter-spacing:.08em; display:block; line-height:1.1; }
.brand small { color:var(--muted); font-size:12px; }

.hero { background: linear-gradient(135deg, var(--accent), var(--accent-2)); color:#fff; border-radius:16px; padding:28px; }
.hero h1 { color:#fff !important; margin:6px 0 8px; font-size:30px; }
.hero p { color:rgba(255,255,255,.88); margin:0; }
.hero .eyebrow { color:rgba(255,255,255,.8); }
.hero .brand b { color:#fff; } .hero .brand small { color:rgba(255,255,255,.75); }
.stats { display:flex; gap:12px; margin:18px 0; }
.stat { background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.2); border-radius:12px; padding:10px 14px; flex:1; }
.stat b { font-family:var(--display); font-size:22px; display:block; }
.stat span { font-size:12px; opacity:.85; }
.track .row { display:flex; align-items:center; gap:10px; padding:7px 0; border-top:1px solid rgba(255,255,255,.16); font-size:14px; }
.track .dot { font-family:var(--display); font-weight:700; font-size:11px; background:#fff; color:var(--accent); border-radius:999px; padding:2px 8px; }
.track .m { margin-left:auto; font-weight:600; }
.track .row .muted { color:rgba(255,255,255,.7); }

.candidate b { display:block; font-family:var(--display); }
.candidate span { display:block; color:var(--muted); font-size:13px; }
.timer { font-family:'JetBrains Mono',monospace; font-size:26px; font-weight:500; background:var(--surface-2); border-radius:12px; padding:8px 14px; text-align:center; }
.timer.low { background:var(--bad-soft); color:var(--bad); }
.chips { display:flex; gap:8px; margin:6px 0 4px; }
.chip { flex:1; border-radius:10px; padding:6px 10px; font-size:13px; }
.chip b { font-family:var(--display); font-size:16px; display:block; }
.chip.xp { background:var(--xp-soft); color:var(--xp); }
.chip.streak { background:var(--accent-soft); color:var(--accent); }

.qhead { display:flex; gap:10px; align-items:center; flex-wrap:wrap; margin-bottom:6px; }
.pill { background:var(--accent-soft); color:var(--accent); border:1px solid var(--accent-line); border-radius:999px; padding:3px 10px; font-size:12px; font-weight:700; font-family:var(--display); }
.qhead .qn { color:var(--muted); font-size:13px; }
.qhead .marks { margin-left:auto; font-size:13px; font-weight:600; color:var(--xp); }
.qtext { font-family:var(--display); font-size:20px; font-weight:600; line-height:1.35; margin:4px 0 10px; }
.quote { border-left:3px solid var(--accent); background:var(--surface-2); padding:10px 14px; border-radius:0 10px 10px 0; margin-bottom:10px; font-style:italic; }
.hint { background:var(--xp-soft); color:#7a4a00; border-radius:10px; padding:8px 12px; font-size:14px; margin-bottom:10px; }

/* Question number dots: answered ones are tinted. Streamlit adds .st-key-<key> to keyed elements. */
[class*="st-key-dotans_"] button { background:var(--good-soft) !important; border-color:var(--good) !important; color:var(--good) !important; }
[class*="st-key-dot"] button { padding:2px 0 !important; min-height:32px !important; }
[class*="st-key-dot"] button p { font-size:13px !important; }

.res-hero { display:flex; gap:28px; align-items:center; background:var(--surface); border:1px solid var(--line); border-radius:16px; padding:24px; flex-wrap:wrap; }
.ring { position:relative; width:150px; height:150px; flex:none; }
.ring svg { width:150px; height:150px; transform:rotate(-90deg); }
.ring circle { fill:none; stroke-width:12; }
.ring .trk { stroke:var(--surface-2); } .ring .bar { stroke:var(--accent); stroke-linecap:round; }
.ring .lbl { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; text-align:center; }
.ring .lbl b { font-family:var(--display); font-size:38px; display:block; line-height:1; }
.ring .lbl span { font-size:12px; color:var(--muted); }
.res-meta { flex:1; min-width:260px; }
.res-meta h2 { margin:4px 0 8px !important; font-size:24px; }
.grade-pill { background:var(--accent); color:#fff; border-radius:999px; padding:3px 12px; font-weight:700; font-family:var(--display); margin-right:8px; }
.kv { display:flex; gap:16px; flex-wrap:wrap; font-size:14px; color:var(--muted); margin:10px 0; }
.kv b { color:var(--fg); }
.bar-outer { height:8px; background:var(--surface-2); border-radius:999px; overflow:hidden; }
.bar-outer i { display:block; height:100%; background:var(--accent); border-radius:999px; }
.bar-outer.xp i { background:var(--xp); }
.plabel { display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px; }

.roast { display:flex; gap:16px; background:#fff1ec; border:1px solid #f8cbbd; border-radius:16px; padding:20px; margin:16px 0; }
.roast blockquote { font-family:var(--display); font-size:18px; font-weight:600; margin:6px 0; padding:0; border:0; }
.roast .tag { color:var(--muted); font-size:13px; }
.flame { width:44px; height:44px; flex:none; border-radius:12px; background:var(--coral); display:flex; align-items:center; justify-content:center; }
.flame svg { width:24px; height:24px; fill:#fff; }

.panel { background:var(--surface); border:1px solid var(--line); border-radius:16px; padding:18px; height:100%; }
.panel h3 { font-size:16px; margin:0 0 12px !important; }
.secrow { margin-bottom:12px; }
.secrow .top { display:flex; justify-content:space-between; font-size:14px; }
.secrow small { display:block; color:var(--muted); font-size:12px; }
.notes div { display:flex; gap:8px; font-size:13.5px; margin-top:6px; }
.notes .ok { color:var(--good); font-weight:700; } .notes .no { color:var(--warn); font-weight:700; }
.badges { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.badge { display:flex; gap:10px; align-items:center; font-size:13px; }
.badge .ic { width:36px; height:36px; border-radius:10px; flex:none; display:flex; align-items:center; justify-content:center; }
.badge .ic svg { width:20px; height:20px; fill:none; stroke:#fff; stroke-width:2; stroke-linecap:round; stroke-linejoin:round; }
.badge b { display:block; font-size:13.5px; } .badge span span { color:var(--muted); font-size:12px; }
.badge.locked { opacity:.38; filter:grayscale(1); }

.crit { display:flex; flex-wrap:wrap; gap:6px; margin-top:8px; }
.crit span { border-radius:999px; padding:2px 10px; font-size:12.5px; }
.crit .hit { background:var(--good-soft); color:var(--good); } .crit .miss { background:var(--bad-soft); color:var(--bad); }
.yours { white-space:pre-wrap; background:var(--surface-2); border-radius:10px; padding:10px 12px; font-size:14px; }
@media (max-width: 640px){ .stats{flex-wrap:wrap} .badges{grid-template-columns:1fr} .res-hero{padding:16px} }
</style>
"""


def inject() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


@lru_cache(maxsize=1)
def logo_data_uri() -> str:
    return "data:image/png;base64," + base64.b64encode(LOGO.read_bytes()).decode() if LOGO.exists() else ""


def brand_html() -> str:
    return (f'<div class="brand"><img src="{logo_data_uri()}" alt="">'
            '<div><b>SOCIAL EAGLE</b><small>learn. build. operate</small></div></div>')


def html(markup: str) -> None:
    st.markdown(markup, unsafe_allow_html=True)


e = escape
