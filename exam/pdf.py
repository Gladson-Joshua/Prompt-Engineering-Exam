"""One-page A4 scorecard, laid out like the jsPDF version in the HTML exam."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fpdf import FPDF

from .data import BADGES
from .grading import SCORED_SECTIONS, fmt

LOGO = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
ACCENT, INK, MUTE, SOFT = (181, 32, 47), (24, 24, 24), (100, 100, 110), (251, 235, 237)

# Unicode TTFs to try (regular, bold, italic, bold-italic); fall back to Helvetica + Latin-1.
_FONT_SETS = [
    ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/ariali.ttf", "C:/Windows/Fonts/arialbi.ttf"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf"),
]
_ASCII = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "—": "-", "–": "-", "→": "->", "…": "..."})


class _Card(FPDF):
    def setup_font(self) -> None:
        self.family, self.unicode = "helvetica", False
        for fs in _FONT_SETS:
            if all(Path(f).exists() for f in fs):
                for style, f in zip(("", "B", "I", "BI"), fs):
                    self.add_font("card", style, f)
                self.family, self.unicode = "card", True
                return

    def t(self, s: str) -> str:
        if self.unicode:
            return s
        return s.translate(_ASCII).encode("latin-1", "replace").decode("latin-1")

    def f(self, style: str = "", size: float = 10, color=INK) -> None:
        self.set_font(self.family, style, size)
        self.set_text_color(*color)

    def txt(self, x: float, y: float, s: str, align: str = "L") -> None:
        s = self.t(s)
        if align == "R":
            x -= self.get_string_width(s)
        self.text(x, y, s)


def build_scorecard(user: dict, r: dict) -> bytes:
    W, M = 210, 16
    pdf = _Card(unit="mm", format="A4")
    pdf.set_auto_page_break(False)
    pdf.add_page()
    pdf.setup_font()

    # Header band
    pdf.set_fill_color(*ACCENT)
    pdf.rect(0, 0, W, 34, "F")
    pdf.f("B", 20, (255, 255, 255)); pdf.txt(M, 15, "SOCIAL EAGLE")
    if LOGO.exists():
        pdf.image(str(LOGO), W - M - 24, 5, 24, 24)
    pdf.f("", 11, (255, 255, 255)); pdf.txt(M, 23, "Prompt Engineering Exam · Scorecard")
    when = datetime.fromisoformat(r["date"]).astimezone().strftime("%d %b %Y, %I:%M %p")
    pdf.f("", 9, (255, 255, 255)); pdf.txt(W - M - 28, 23, when, "R")

    # Candidate
    y = 46
    pdf.f("B", 16); pdf.txt(M, y, user["name"])
    pdf.f("", 10, MUTE); pdf.txt(M, y + 6, f"{user['email']}   ·   {user['batch']}")

    # Score block
    y = 60
    pdf.set_fill_color(*SOFT)
    pdf.rect(M, y, W - 2 * M, 36, "F", round_corners=True, corner_radius=3)
    big = fmt(r["total"])
    pdf.f("B", 40, ACCENT); pdf.txt(M + 8, y + 26, big)
    bw = pdf.get_string_width(big)
    pdf.f("", 12, MUTE); pdf.txt(M + 8 + bw + 3, y + 26, "/ 100")
    pdf.f("B", 13); pdf.txt(M + 70, y + 14, f"Grade {r['grade']}"); pdf.txt(M + 70, y + 22, f"Rank: {r['level']}")
    mins = int(r["minutes"]); secs = round((r["minutes"] % 1) * 60)
    pdf.f("", 10, MUTE)
    pdf.txt(M + 70, y + 30, f"{r['xp']} XP   ·   {r['answered']}/50 answered   ·   {mins} min {secs} s   ·   {r['keywords']}/10 keywords")

    # Level breakdown
    y = 106
    pdf.f("B", 12); pdf.txt(M, y, "Level breakdown")
    y += 6
    for i, s in enumerate(SCORED_SECTIONS):
        got = r["sections"][s.id]; p = got / s.marks
        if i % 2 == 0:
            pdf.set_fill_color(250, 246, 246); pdf.rect(M, y, W - 2 * M, 11, "F")
        pdf.f("B", 10); pdf.txt(M + 3, y + 5, f"L{s.level}  {s.name}")
        pdf.f("", 8.5, MUTE); pdf.txt(M + 3, y + 9, s.sub)
        bx, bwid = M + 90, 60
        pdf.set_fill_color(*SOFT); pdf.rect(bx, y + 3.5, bwid, 4, "F", round_corners=True, corner_radius=2)
        if p > 0:
            pdf.set_fill_color(*ACCENT); pdf.rect(bx, y + 3.5, max(4, bwid * p), 4, "F", round_corners=True, corner_radius=2)
        pdf.f("B", 10); pdf.txt(W - M - 3, y + 7, f"{fmt(got)} / {s.marks}", "R")
        y += 11

    # Badges
    y += 10
    pdf.f("B", 12); pdf.txt(M, y, "Badges earned")
    y += 7
    earned = [b for b in BADGES if b.id in r["badges"]]
    if not earned:
        pdf.f("", 9.5, MUTE); pdf.txt(M, y, "No badges this attempt. Retake to earn some.")
        y += 6
    else:
        x = M
        pdf.f("B", 9.5, (255, 255, 255))
        for b in earned:
            w = pdf.get_string_width(pdf.t(b.name)) + 10
            if x + w > W - M:
                x = M; y += 9
            pdf.set_fill_color(*ACCENT)
            pdf.rect(x, y - 5, w, 7.5, "F", round_corners=True, corner_radius=3.5)
            pdf.txt(x + 5, y, b.name)
            x += w + 4
        y += 10

    # Roast
    y += 6
    pdf.set_fill_color(255, 241, 236)
    pdf.rect(M, y, W - 2 * M, 34, "F", round_corners=True, corner_radius=3)
    pdf.f("B", 9, (226, 85, 79)); pdf.txt(M + 6, y + 8, f"THE ROAST  ·  {r['roast_tag'].upper()}")
    pdf.f("BI", 12)
    pdf.set_xy(M + 6, y + 12)
    pdf.multi_cell(W - 2 * M - 12, 6, pdf.t(f"“{r['roast']}”"))

    # Footer
    pdf.set_draw_color(230, 215, 217); pdf.line(M, 278, W - M, 278)
    pdf.f("", 8, MUTE)
    pdf.txt(M, 284, "Social Eagle · learn. build. operate · MCQs auto-marked; written answers graded by keyword rubric, subject to trainer moderation.")
    pdf.txt(M, 289, "RTCFR · Prompt Chaining · CoT · ToT · ReAct · Multi-Agent · Prompt Injection · Reverse Prompting")
    return bytes(pdf.output())
