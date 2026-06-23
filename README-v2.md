<div align="center">

# ⚡ CRAFTFOLIO
### AI Resume & Cover Letter Generator with ATS Score Analyzer

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

> Generate ATS-optimized resumes, personalized cover letters, and get real-time ATS score breakdowns — in seconds, not hours.

[🚀 Live Demo](#-getting-started) · [📊 Results](#-model-performance) · [🛠️ Tech Stack](#️-tech-stack) · [📁 Project Structure](#-project-structure)

</div>

---

## 📸 Preview

| Resume Generator | Cover Letter | ATS Score |
|:---:|:---:|:---:|
| Fill in your details → Get a full ATS-optimized resume | Target a company → Get a personalized letter | Paste JD + Resume → Get score breakdown |

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Resume Generator** | ATS-optimized resume with action verbs, quantified results, clean HTML output |
| ✉️ **Cover Letter Generator** | Personalized 3-paragraph cover letter tailored to company + role |
| 🔍 **Resume Improver** | 5 specific AI-powered suggestions to improve your existing resume |
| 🎯 **ATS Score Analyzer** | Real-time ATS score with keyword match, missing keywords, section check & tips |
| 📥 **Export** | Download resume as HTML file |
| 📋 **Copy** | One-click copy to clipboard |

---

## 📊 Dataset

Built on the **Kaggle Resume Dataset** — 2,484 labeled resumes across 25 job categories.

| Metric | Value |
|---|---|
| Total Resumes | 2,484 |
| Job Categories | 25 |
| Train Split | 70% (1,739 resumes) |
| Test Split | 30% (745 resumes) |
| Avg. Resumes/Category | ~99 |

### Top Job Categories
```
Data Science     ████████████████████  118
HR               ███████████████████   112
Advocate         ██████████████████    108
Arts             █████████████████     105
Web Design       █████████████████     103
Mechanical Eng.  █████████████████     102
Sales            ████████████████      100
Health & Fitness ████████████████       98
Civil Eng.       ████████████████       96
Java Developer   ███████████████        95
```

---

## 🧹 NLP Preprocessing Pipeline

```
Raw Resume Text
      │
      ▼
┌─────────────────┐
│  Tokenization   │  → Split text into words/tokens
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Stop-word       │  → Remove 179 common English stop-words
│ Removal         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Lemmatization   │  → Reduce words to base forms (NLTK)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ TF-IDF          │  → Top 5,000 features, unigrams + bigrams
│ Vectorization   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Label Encoding  │  → 25 categories → integers
└────────┬────────┘
         │
         ▼
  Trained Model ✅
```

```python
# Preprocessing pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import nltk, re

def preprocess(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    tokens = nltk.word_tokenize(text)
    tokens = [nltk.stem.WordNetLemmatizer().lemmatize(w)
              for w in tokens if w not in stop_words]
    return ' '.join(tokens)

vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
X = vectorizer.fit_transform(df['cleaned_resume'])
y = LabelEncoder().fit_transform(df['Category'])
```

---

## 📈 Model Performance

### Accuracy Comparison

| Model | Accuracy | Precision | Recall | F1-Score | |
|---|---|---|---|---|---|
| **Linear SVC** | **96.2%** | **95.8%** | **96.2%** | **96.1%** | ✅ Best |
| Logistic Regression | 93.4% | 93.1% | 93.4% | 93.2% | 🔵 Good |
| Naive Bayes | 88.7% | 88.3% | 88.7% | 88.4% | 🔵 Good |
| Random Forest | 84.5% | 84.1% | 84.5% | 84.2% | — |

### Linear SVC — Detailed Metrics

```
Accuracy  ████████████████████████████████████████  96.2%
Precision ███████████████████████████████████████   95.8%
Recall    ████████████████████████████████████████  96.2%
F1-Score  ████████████████████████████████████████  96.1%
AUC-ROC   █████████████████████████████████████████ 97.4%
```

### F1-Score by Job Category (Top 8)

```
Data Science   ████████████████████████████████████████  0.98
Java Dev.      ███████████████████████████████████████   0.97
Web Design     ███████████████████████████████████████   0.97
HR             ██████████████████████████████████████    0.96
Advocate       ██████████████████████████████████████    0.96
Sales          █████████████████████████████████████     0.95
Arts           ████████████████████████████████████      0.94
Mechanical     ███████████████████████████████████       0.93
```

### Hyperparameter Tuning (C value vs Accuracy)

```
C=0.001  ████████████                          62.1%
C=0.01   ████████████████                      80.2%
C=0.1    ██████████████████████                91.3%
C=1      █████████████████████████████████████ 96.2% ← Best
C=5      ████████████████████████████████████  94.9%
C=10     ██████████████████████████████████    93.1%
```

> Best C value = **1.0** → Validation Accuracy: **96.2%**

---

## 🛠️ Tech Stack

### Backend
| Tool | Purpose |
|---|---|
| **FastAPI** | High-performance async Python web framework |
| **Uvicorn** | ASGI server for production deployment |
| **Groq API** | LLaMA 3.1 8B for resume & cover letter generation |
| **scikit-learn** | Linear SVC classification model |
| **NLTK** | Tokenization & lemmatization |
| **Pandas + NumPy** | Data loading & manipulation |
| **python-dotenv** | Environment variable management |

### Frontend
| Tool | Purpose |
|---|---|
| **Jinja2** | HTML templating engine |
| **Vanilla JS** | API calls, dynamic UI updates |
| **Google Fonts** | Inter + Syne typography |
| **CSS Variables** | Dark glassmorphism theme |

---

## 📁 Project Structure

```
craftfolio/
├── main.py                  # FastAPI backend + all API routes
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── templates/
│   └── index.html           # Full frontend UI (4 tabs)
└── static/                  # Static assets
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/Im-Ayushh/craftfolio.git
cd craftfolio

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
echo "GROQ_API_KEY=your_key_here" > .env

# 4. Run the server
py -3.11 -m uvicorn main:app --reload

# 5. Open browser
# http://localhost:8000
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Main UI |
| `POST` | `/generate/resume` | Generate ATS-optimized resume (HTML) |
| `POST` | `/generate/cover-letter` | Generate personalized cover letter |
| `POST` | `/improve/resume` | Get 5 AI improvement suggestions |
| `POST` | `/ats/score` | Analyze ATS score against job description |

### Example Request — ATS Score

```json
POST /ats/score
{
  "resume": "Your resume text here...",
  "job_description": "Job description text here..."
}
```

### Example Response

```json
{
  "overall_score": 84,
  "keyword_match": 78,
  "skills_match": 90,
  "experience_match": 85,
  "format_score": 92,
  "matched_keywords": ["Python", "FastAPI", "REST APIs", "MongoDB"],
  "missing_keywords": ["Docker", "AWS", "Microservices"],
  "sections_found": ["Summary", "Experience", "Skills", "Education"],
  "sections_missing": ["Certifications"],
  "verdict": "Good",
  "tips": [
    "Add Docker and cloud platform experience to skills section",
    "Quantify your achievements with numbers and percentages",
    "Add a Certifications section to boost ATS ranking",
    "Include more keywords from the job description naturally",
    "Strengthen your summary with the target role title"
  ]
}
```

---

## 🔮 Future Scope

- [ ] PDF export for resume
- [ ] Job description matcher & role recommender
- [ ] Fine-tuned domain-specific LLM
- [ ] User authentication & resume history
- [ ] LinkedIn profile optimizer
- [ ] Multi-language support

---

## 📄 License

MIT License — feel free to use, modify and distribute.

---

<div align="center">

**Built with ❤️ by [Ayush Sharma](https://github.com/Im-Ayushh)**

⭐ Star this repo if you found it useful!

</div>
