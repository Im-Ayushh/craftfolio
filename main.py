from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

app = FastAPI(title="CRAFTFOLIO — AI Resume & Cover Letter Generator")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"


class ResumeRequest(BaseModel):
    name: str
    email: str
    phone: str
    role: str
    experience: str
    skills: str
    education: str
    achievements: str


class CoverLetterRequest(BaseModel):
    name: str
    role: str
    company: str
    experience: str
    skills: str
    why_company: str


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate/resume")
async def generate_resume(data: ResumeRequest):
    try:
        prompt = f"""You are an expert resume writer. Generate a professional, ATS-optimized resume in clean HTML format (no <html>/<body> tags, just the content).

Candidate Details:
- Name: {data.name}
- Email: {data.email}
- Phone: {data.phone}
- Target Role: {data.role}
- Experience: {data.experience}
- Skills: {data.skills}
- Education: {data.education}
- Achievements: {data.achievements}

Generate a modern, structured resume with sections: Summary, Experience, Skills, Education, Achievements.
Use <h1>, <h2>, <h3>, <p>, <ul>, <li> tags only. Make it ATS-friendly and impactful.
Write powerful bullet points with action verbs and quantified results where possible.
Return ONLY the HTML content, no markdown, no code blocks, no extra explanation."""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.7,
        )
        return {"html": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/cover-letter")
async def generate_cover_letter(data: CoverLetterRequest):
    try:
        prompt = f"""You are an expert career coach. Write a compelling, personalized cover letter.

Details:
- Candidate: {data.name}
- Target Role: {data.role}
- Company: {data.company}
- Experience: {data.experience}
- Key Skills: {data.skills}
- Why this company: {data.why_company}

Write a 3-paragraph cover letter:
1. Strong opening hook + role interest
2. Relevant experience and value proposition
3. Why this company + call to action

Make it confident, specific, and human. No clichés. Return plain text only, no markdown."""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.75,
        )
        return {"text": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/improve/resume")
async def improve_resume(data: dict):
    try:
        prompt = f"""You are an expert resume reviewer. Analyze this resume and provide exactly 5 specific, actionable improvements.

Resume Content:
{data.get('content', '')}

Target Role: {data.get('role', 'Not specified')}

Return exactly 5 bullet points, each starting with a relevant emoji and an action verb.
Be specific and direct, not generic. No extra explanation."""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.6,
        )
        return {"suggestions": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ats/score")
async def ats_score(data: dict):
    try:
        prompt = f"""You are an expert ATS (Applicant Tracking System) analyzer. Analyze the resume against the job description and return ONLY a valid JSON object, nothing else.

RESUME:
{data.get('resume', '')}

JOB DESCRIPTION:
{data.get('job_description', '')}

Return ONLY this JSON structure with no extra text, no markdown, no code blocks:
{{
  "overall_score": <number 0-100>,
  "keyword_match": <number 0-100>,
  "format_score": <number 0-100>,
  "experience_match": <number 0-100>,
  "skills_match": <number 0-100>,
  "matched_keywords": [<list of up to 10 keywords found in both resume and JD>],
  "missing_keywords": [<list of up to 10 important keywords from JD missing in resume>],
  "sections_found": [<list of resume sections detected e.g. "Summary", "Experience", "Skills", "Education">],
  "sections_missing": [<list of important sections missing>],
  "tips": [<list of exactly 5 specific actionable improvement tips as strings>],
  "verdict": "<one of: Excellent, Good, Needs Work, Poor>"
}}"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.3,
        )

        import json
        raw = response.choices[0].message.content.strip()
        # strip any accidental markdown fences
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
