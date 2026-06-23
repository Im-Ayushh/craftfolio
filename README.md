# CRAFTFOLIO — AI Resume & Cover Letter Generator

A full-stack GenAI web app built with **FastAPI + GPT-4o** with a dark glassmorphism UI.

## Tech Stack
- **Backend:** FastAPI (Python)
- **AI:** OpenAI GPT-4o
- **Frontend:** Vanilla HTML/CSS/JS (dark glassmorphism + minimalist black)
- **Server:** Uvicorn

## Features
- ✅ AI Resume Generator (ATS-optimized, HTML export)
- ✅ AI Cover Letter Generator (personalized per company)
- ✅ Resume Improver (5 specific AI suggestions)
- ✅ Copy to clipboard + Export as HTML
- ✅ Responsive dark UI

## Setup & Run

### 1. Clone & Install
```bash
cd ai-resume-v2
pip install -r requirements.txt
```

### 2. Set your OpenAI API Key
Create a `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the server
```bash
uvicorn main:app --reload
```

### 4. Open in browser
```
http://localhost:8000
```

## Project Structure
```
ai-resume-v2/
├── main.py              # FastAPI backend + API routes
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── templates/
│   └── index.html       # Full frontend UI
└── static/              # Static assets (if any)
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main UI |
| POST | `/generate/resume` | Generate resume HTML |
| POST | `/generate/cover-letter` | Generate cover letter |
| POST | `/improve/resume` | Get 5 AI improvement tips |

## Built for
IBM NTCC Internship — Generative AI Project (Project 2)
