# AI Resume Analyzer

An AI-powered Resume Analyzer that evaluates resumes against job descriptions using Large Language Models (LLMs). It generates an ATS-style score, detects missing skills, and provides intelligent improvement suggestions to help candidates optimize their resumes for job applications.

---

## Features

- ATS Score (0–100) based on resume and job description match
- AI-powered analysis using Groq LLaMA3 model
- Skill extraction and matching
- Missing skill detection
- Smart feedback and improvement suggestions
- Fast Streamlit web application
- Secure API key handling using .env file

---

## Tech Stack

- Python
- Streamlit
- Groq API (LLaMA 3)
- Prompt Engineering
- PDF Processing (PyPDF)
- Hybrid ATS Scoring (LLM + Keyword Matching)
- Environment Management (python-dotenv)
- Git & GitHub

---

## Project Structure

AI-Resume-Analyzer/
├── app.py                Main Streamlit application
├── utils.py              AI logic and Groq API integration
├── requirements.txt      Python dependencies
├── .env.example          Example environment file
├── .gitignore           Ignored files for security
└── README.md            Project documentation

---

## Setup Instructions

1. Clone the repository

git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer

---

2. Create virtual environment

python -m venv venv

Activate:
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

---

3. Install dependencies

pip install -r requirements.txt

---

4. Add environment variables

Create a file named .env in root folder:

GROQ_API_KEY=your_groq_api_key_here

---

5. Run the application

streamlit run app.py

---

## Example Output

{
  "ATS Score": 85,
  "Matched Skills": ["Python", "Machine Learning", "Pandas"],
  "Missing Skills": ["Docker", "AWS"],
  "Feedback": "Good resume but lacks deployment and cloud experience."
}

---

## How It Works

1. User uploads or pastes resume
2. User enters job description
3. Both are sent to Groq LLM
4. AI analyzes:
   - Skill matching
   - Missing keywords
   - ATS scoring
5. Results displayed in UI

---

## Future Improvements

- PDF resume parsing
- Multi-page resume support
- Downloadable ATS report
- Cloud deployment (Streamlit / Render)
- Role-based scoring system

---

## License

This project is for educational and portfolio purposes
