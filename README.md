# Social Eagle Prompt Engineering Exam

A browser-based prompt engineering assessment with five levels, timed progress, automatic scoring, answer feedback, and a downloadable scorecard.

## Run the exam

1. Open `Social_Eagle_Prompt_Exam.html` in a recent web browser.
2. Enter your name, email address, and batch/class.
3. Select **Enter the exam**. The 90-minute timer starts when the exam begins.
4. Navigate between questions and levels, then select **Finish exam** to submit.
5. Review your score and feedback. Download the scorecard as a PDF, copy the summary, or retake the exam.

No installation, build step, or server is required. An internet connection is used to load Google Fonts and the jsPDF library; the page falls back to the browser's print dialog if the PDF library is unavailable.

## Exam contents

| Level | Section | Questions | Scoring |
|---|---|---:|---:|
| 1 | RTCFR & techniques | 20 multiple-choice | 20 marks |
| 2 | Short answers | 15 written | 30 marks |
| 3 | Write prompts | 10 written | 30 marks |
| 4 | Identify RTCFR | 5 written | 10 marks |
| 5 | Keyword Vault | 10 keywords | XP bonus |

Written answers are evaluated against in-page rubrics. The results screen includes a level breakdown, feedback, badges, and an answer review.

**Scoring note:** The scored sections currently add up to 90 marks, although the results screen labels the score as `/100`. The Keyword Vault contributes XP, not marks.

## Progress and privacy

An in-progress attempt is saved in the browser's local storage so it can be resumed in that browser. Candidate details and answers are not sent to an application server by this page. Retaking the exam clears the saved attempt in that browser. Clearing site data or using a different browser/device removes access to the saved attempt.

The page requests external assets from Google Fonts and cdnjs (jsPDF). Avoid entering sensitive personal information.

## Streamlit version

A Python/Streamlit port of the same exam lives alongside the HTML file. It uses the same questions, rubrics, scoring, XP, badges, roasts and PDF scorecard.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\streamlit run app.py
```

Differences from the HTML version:

- Attempts are saved on the server in `data/attempts/` (one JSON file per email, named by a hash of the email). The page URL carries the attempt key, so refreshing the browser resumes the attempt. Registering again with the same email offers **Resume** or **Start a new attempt**.
- Written answers save when the candidate clicks outside the box, clicks a button, or presses Ctrl+Enter.
- "Copy summary" opens a box with a copy icon; confetti is Streamlit's balloons.

| Path | Purpose |
|---|---|
| `app.py` | Entry point; chooses the register, exam or results screen. |
| `exam/data.py` | Question bank, answer key, rubrics, levels, badges, roasts. Edit questions here. |
| `exam/grading.py`, `exam/xp.py` | Scoring and live XP rules (no Streamlit code). |
| `exam/store.py`, `exam/pdf.py` | Attempt storage and the PDF scorecard. |
| `ui/` | The three screens and the theme. |
| `tests/` | `pytest` suite, including 360 cases checked against the original JavaScript grader. |

Run the tests with `.\.venv\Scripts\python -m pytest -q`.

## Project files

- `Social_Eagle_Prompt_Exam.html` — the complete application, including styles, exam questions, scoring, and interface logic.
- `README.md` — setup and usage information.
