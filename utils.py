from groq import Groq
from pypdf import PdfReader
import os
import re

client = Groq(api_key = os.getenv("GROQ_API_KEY"))

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract plain text from an uploaded PDF file using PyPDF.

    Args:
        uploaded_file: A file-like object (e.g. from st.file_uploader).

    Returns:
        Full extracted text from all pages as a single string.
        Returns an empty string if no text could be extracted.
    """
    reader = PdfReader(uploaded_file)
    extracted_pages = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:                          # skip blank/image-only pages
            extracted_pages.append(page_text)

    return "\n".join(extracted_pages).strip()


def analyze_resume(resume_text: str, job_description: str) -> dict:
    """
    Send resume + job description to Groq and return structured feedback.
    Returns a markdown-formatted string with suggestions.
    """

    prompt = f"""You are a senior career coach with 15 years of experience helping candidates land roles at top companies.
 
    A candidate has asked you to review their resume against a job description.
    
    RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {job_description}
    
    Your task is to return a structured analysis in EXACTLY this format. Do not add any extra text outside this format.
    
    MATCHED SKILLS:
    - skill1
    - skill2
    - skill3
    
    MISSING SKILLS:
    - skill1
    - skill2
    - skill3
    
    SUGGESTIONS:
    - Title of suggestion | Write 2-3 sentences of specific, human, actionable advice. Reference the actual job description and the candidate's background. Tell them exactly what to do, not just what is missing. Be direct but encouraging — like a mentor who genuinely wants them to succeed.
    - Title of suggestion | Write 2-3 sentences of specific, human, actionable advice. Reference the actual job description and the candidate's background. Tell them exactly what to do, not just what is missing. Be direct but encouraging — like a mentor who genuinely wants them to succeed.
    - Title of suggestion | Write 2-3 sentences of specific, human, actionable advice. Reference the actual job description and the candidate's background. Tell them exactly what to do, not just what is missing. Be direct but encouraging — like a mentor who genuinely wants them to succeed.
    
    Rules for SUGGESTIONS:
    - Each suggestion must have a short bold title (3-5 words), followed by " | ", followed by the detailed advice
    - Advice must be specific to THIS resume and THIS job — no generic tips
    - Mention specific skills, tools, or experiences from the resume or JD
    - If a skill is missing, tell them exactly how to demonstrate it (course, project, GitHub, etc.)
    - If something exists but is weak, tell them how to strengthen it with metrics or context
    - Write like a human, not a robot. Avoid bullet-within-bullet, avoid vague phrases like "consider improving"
    
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        #max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
        temperature = 0.6,
    )

    #response_text = response.choices[0].message.content.strip()

    text = response.choices[0].message.content

    matched, missing, suggestions = [], [], []
    current = None

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        upper = line.upper()

        # Section headers — only match lines that ARE the header (≤ 40 chars)
        # This prevents skill descriptions containing these words from resetting state

        if len(line)<=40:
            if "MATCHED SKILLS" in upper:
                current = "matched"
                continue
            elif "MISSING SKILLS" in upper:
                current = "missing"
                continue
            elif re.search(r"\bSUGGESTIONS\b", upper):
                current = "suggestions"
                continue
        
        # Strip any leading bullet/number: "- ", "1. ", "2. ", "* " etc.
        cleaned = re.sub(r"^[-*\d]+[.)]\s*", "", line).strip()
        if not cleaned:
            continue

        is_bullet = bool(re.match(r"^[-*•\d]", line))
 
        if current == "matched" and is_bullet:
            matched.append(cleaned)
        elif current == "missing" and is_bullet:
            missing.append(cleaned)
        elif current == "suggestions":
            # Accept dash bullets, numbered lines, or any line containing | separator
            if re.match(r"^[-*\d]", line) or "|" in line:
                suggestions.append(cleaned)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "improvement_suggestions": suggestions
        }



def get_match_score(resume_text: str, job_description: str) -> int:
    """
    Ask Groq to estimate a compatibility score (0-100) between
    the resume and job description.
    Returns an integer score.
    """

    prompt = f"""You are a resume screening tool.
    
    Given this resume:
    <resume>
    {resume_text}
    </resume>

    And this job description:
    <job_description>
    {job_description}
    </job_description>

    Respond with ONLY a single integer from 0 to 100 representing how well the resume matches the job.
    Do not include any explanation, just the number."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        #max_tokens=10,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()

    # Safely parse the score
    try:
        score = int("".join(filter(str.isdigit, raw)))
        return min(max(score, 0), 100)  # clamp between 0 and 100
    except ValueError:
        return 0