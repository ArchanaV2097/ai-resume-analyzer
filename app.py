import streamlit as st
from utils import extract_text_from_pdf, analyze_resume, get_match_score

st.set_page_config(
    page_title="ResumeIQ · AI Resume Analyzer",
    page_icon="✦",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@300;400;500;600&display=swap');

:root {
    --bg:          #f7f6f3;
    --surface:     #ffffff;
    --surface2:    #f0eeea;
    --border:      #e4e1da;
    --border-hi:   #c9c5bc;
    --text:        #1a1917;
    --muted:       #7c7870;
    --green:       #16a34a;
    --green-dim:   #dcfce7;
    --green-ring:  #bbf7d0;
    --amber:       #b45309;
    --amber-dim:   #fef3c7;
    --amber-ring:  #fde68a;
    --red:         #dc2626;
    --red-dim:     #fee2e2;
    --red-ring:    #fecaca;
    --accent:      #4f46e5;
    --accent-soft: #eef2ff;
    --accent-ring: #c7d2fe;
    --radius:      14px;
    --shadow:      0 1px 4px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.05);
}

html, body, [class*="css"] {
    font-family: 'Geist', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 3.5rem !important;
    padding-bottom: 5rem !important;
    max-width: 720px !important;
}

/* ── Header ── */
.header { text-align: center; padding-bottom: 3rem; }
.header h1 {
    font-family: 'Instrument Serif', serif;
    font-size: 3rem;
    font-weight: 400;
    line-height: 1.1;
    letter-spacing: -1.5px;
    color: var(--text);
    margin: 0 0 0.7rem;
}
.header h1 em { font-style: italic; color: var(--accent); }
.header p {
    font-size: 1rem;
    font-weight: 300;
    color: var(--muted);
    margin: 0;
    line-height: 1.65;
}

/* ── Input cards ── */
.input-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.6rem;
}

[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1.5px dashed var(--border-hi) !important;
    border-radius: 10px !important;
    padding: 0.4rem 0.6rem !important;
    transition: border-color 0.2s !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stFileUploader"]:hover { border-color: var(--accent) !important; }
[data-testid="stFileUploader"] * { color: var(--text) !important; }
[data-testid="stFileUploader"] small { color: var(--muted) !important; }

textarea {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Geist', sans-serif !important;
    font-size: 0.9rem !important;
    line-height: 1.65 !important;
    resize: vertical !important;
    box-shadow: var(--shadow) !important;
    transition: border-color 0.2s !important;
}
textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-ring) !important;
    outline: none !important;
}
textarea::placeholder { color: #b0ada6 !important; }

/* ── Button ── */
div.stButton > button {
    width: 100% !important;
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.82rem 1.6rem !important;
    font-family: 'Geist', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1px !important;
    box-shadow: 0 2px 8px rgba(79,70,229,0.25) !important;
    transition: opacity 0.15s, transform 0.1s !important;
}
div.stButton > button:hover  { opacity: 0.88 !important; transform: translateY(-1px) !important; }
div.stButton > button:active { transform: translateY(0) !important; }

/* ── Result card ── */
.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 2rem;
    margin-top: 1.6rem;
    box-shadow: var(--shadow);
}

/* Score row */
.score-wrapper {
    display: flex;
    align-items: center;
    gap: 1.8rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.score-number {
    font-family: 'Instrument Serif', serif;
    font-size: 4.2rem;
    line-height: 1;
    min-width: 110px;
}
.score-right { flex: 1; }
.score-badge {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    border-radius: 999px;
    padding: 0.28rem 0.85rem;
    margin-bottom: 0.5rem;
}
.badge-green { background: var(--green-dim); color: var(--green); border: 1px solid var(--green-ring); }
.badge-amber { background: var(--amber-dim); color: var(--amber); border: 1px solid var(--amber-ring); }
.badge-red   { background: var(--red-dim);   color: var(--red);   border: 1px solid var(--red-ring);   }
.score-desc  { font-size: 0.88rem; color: var(--muted); line-height: 1.55; }

/* Progress bar */
.progress-track {
    height: 5px;
    background: var(--surface2);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 0.75rem;
}
.progress-fill { height: 100%; border-radius: 999px; }

/* Section titles */
.section-title {
    font-size: 0.67rem;
    font-weight: 600;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: var(--muted);
    margin: 1.5rem 0 0.7rem;
}

/* Pills */
.pill-row { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.pill { font-size: 0.8rem; font-weight: 500; padding: 0.3rem 0.8rem; border-radius: 999px; }
.pill-green { background: var(--green-dim); color: var(--green); border: 1px solid var(--green-ring); }
.pill-red   { background: var(--red-dim);   color: var(--red);   border: 1px solid var(--red-ring);   }
.pill-empty { color: var(--muted); font-size: 0.82rem; font-style: italic; }

/* Suggestions */
.suggestion-item {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    padding: 1rem 0;
    border-bottom: 1px solid var(--border);
}
.suggestion-item:last-child { border-bottom: none; padding-bottom: 0; }
.suggestion-num {
    font-family: 'Instrument Serif', serif;
    font-size: 1.1rem;
    color: var(--accent);
    min-width: 22px;
    padding-top: 1px;
    line-height: 1.5;
    flex-shrink: 0;
}
.suggestion-text {
    font-size: 0.91rem;
    line-height: 1.7;
    color: var(--text);
}
.suggestion-text strong {
    display: block;
    font-weight: 600;
    margin-bottom: 0.2rem;
    color: var(--text);
    font-size: 0.92rem;
}
.suggestion-text span {
    color: var(--muted);
    font-size: 0.87rem;
}

/* Empty state */
.empty-state { text-align: center; padding: 3.5rem 1rem; color: var(--muted); }
.empty-icon  { font-size: 2rem; margin-bottom: 0.7rem; opacity: 0.3; }
.empty-state p { font-size: 0.9rem; line-height: 1.65; max-width: 320px; margin: 0 auto; }

[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-size: 0.88rem !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def render_pills(items: list, color: str) -> str:
    if not items:
        return '<span class="pill-empty">None identified</span>'
    inner = "".join(f'<span class="pill pill-{color}">{s}</span>' for s in items)
    return f'<div class="pill-row">{inner}</div>'


def render_suggestions(items: list) -> str:
    if not items:
        return '<p class="pill-empty">No suggestions returned.</p>'
    rows = ""
    for i, tip in enumerate(items, 1):
        # Split on " | " if the model returned "Title | detail" format
        if " | " in tip:
            title, detail = tip.split(" | ", 1)
        else:
            title = tip
            detail = ""
        detail_html = f"<span>{detail}</span>" if detail else ""
        rows += (
            f'<div class="suggestion-item">'
            f'  <span class="suggestion-num">{i}.</span>'
            f'  <div class="suggestion-text"><strong>{title}</strong>{detail_html}</div>'
            f'</div>'
        )
    return rows


def score_meta(score: int) -> tuple:
    if score >= 75:
        return "#16a34a", "badge-green", "Strong Match", \
            "Your resume aligns well with this role. A few targeted tweaks could push you to the top of the pile."
    elif score >= 50:
        return "#b45309", "badge-amber", "Partial Match", \
            "You meet several requirements but there are meaningful gaps. Focus on the missing skills below."
    else:
        return "#dc2626", "badge-red", "Low Match", \
            "Significant gaps exist between your profile and this role. Consider upskilling or targeting a closer fit."


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header">
    <h1>Resume<em>IQ</em></h1>
    <p>Drop your resume, paste the job description.<br>
    Get a match score, skill gaps, and concrete next steps &mdash; instantly.</p>
</div>
""", unsafe_allow_html=True)

# ── Resume upload ─────────────────────────────────────────────────────────────
st.markdown('<div class="input-label">📄 Your Resume</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    label="resume", type=["pdf"],
    label_visibility="collapsed",
    help="Text-based PDF only · Max 10 MB",
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Job description ───────────────────────────────────────────────────────────
st.markdown('<div class="input-label">💼 Job Description</div>', unsafe_allow_html=True)
job_description = st.text_area(
    label="jd",
    label_visibility="collapsed",
    height=200,
    placeholder="Paste the full job description — role summary, requirements, responsibilities, nice-to-haves…",
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Analyze button ────────────────────────────────────────────────────────────
analyze_clicked = st.button("✦ Analyze My Resume")

# ── Empty state ───────────────────────────────────────────────────────────────
if not analyze_clicked:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">◎</div>
        <p>Your analysis will appear here.<br>Upload a resume and paste a job description to get started.</p>
    </div>
    """, unsafe_allow_html=True)

# ── Analysis + results ────────────────────────────────────────────────────────
if analyze_clicked:
    if not uploaded_file:
        st.warning("Please upload your resume as a PDF first.")
    elif not job_description.strip():
        st.warning("Please paste a job description before analyzing.")
    else:
        try:
            with st.spinner("Reading resume and running analysis…"):
                resume_text = extract_text_from_pdf(uploaded_file)
                if not resume_text.strip():
                    st.error("No text found in the PDF. Make sure it's a text-based file, not a scanned image.")
                    st.stop()
                result = analyze_resume(resume_text, job_description)
                score  = get_match_score(resume_text, job_description)

            color, badge_cls, verdict, desc = score_meta(score)
            pills_matched = render_pills(result.get("matched_skills", []), "green")
            pills_missing = render_pills(result.get("missing_skills", []), "red")
            suggestions   = render_suggestions(result.get("improvement_suggestions", []))

            st.markdown(
                f'<div class="result-card">'
                f'<div class="score-wrapper">'
                f'  <div class="score-number" style="color:{color}">{score}%</div>'
                f'  <div class="score-right">'
                f'    <span class="score-badge {badge_cls}">{verdict}</span>'
                f'    <div class="score-desc">{desc}</div>'
                f'    <div class="progress-track">'
                f'      <div class="progress-fill" style="width:{score}%;background:{color}"></div>'
                f'    </div>'
                f'  </div>'
                f'</div>'
                f'<div class="section-title">✅ Matched Skills</div>'
                f'{pills_matched}'
                f'<div class="section-title">⚠️ Missing Skills</div>'
                f'{pills_missing}'
                f'<div class="section-title">💡 Improvement Suggestions</div>'
                f'{suggestions}'
                f'</div>',
                unsafe_allow_html=True
            )

        except ValueError as exc:
            st.error(f"Configuration error: {exc}")
        except Exception as exc:
            st.error(f"Something went wrong: {exc}")