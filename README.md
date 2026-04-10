<!-- ---
title: Socratic Maths Tutor AI
emoji: 🎓
colorFrom: red
colorTo: gray
sdk: docker
app_port: 3000
pinned: false
license: mit
short_description: Socratic AI-powered mathematics tutoring with image OCR
--- -->

<div align="center">

<img src="https://huggingface.co/datasets/ayushsainime/socratic_maths_tutor_media/resolve/main/female-math-tutor-writes-equations-blackboard-chalk-student-writes-them-down-notebook-vector-413658303.jpg" alt="Socratic Maths Tutor" width="130" height="130" style="border-radius: 24px; border: 3px solid #E63946;" />

# SOCRATIC MATHS TUTOR

*An AI-powered Socratic tutoring system that guides students through handwritten math problems — one thoughtful question at a time.*

[![Live Demo](https://img.shields.io/badge/Live-Demo-E63946?style=for-the-badge&logo=google-chrome&logoColor=white)](https://huggingface.co/spaces/ayushsainime/socratic_maths_tutor.ai)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Reflex](https://img.shields.io/badge/Reflex-0.8.27-00B4D8?style=for-the-badge&logo=react&logoColor=white)](https://reflex.dev)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3-F55036?style=for-the-badge&logoColor=white)](https://groq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-2EA043?style=for-the-badge)](./LICENSE)

</div>

---

## Overview

**Socratic Maths Tutor** is a full-stack AI application that transforms photos of handwritten math into interactive, guided learning sessions. Instead of giving away answers, the AI tutor uses the **Socratic method** — asking targeted questions that help students discover solutions on their own.

The system combines **deep-learning OCR** (Pix2TeX), **symbolic math analysis** (SymPy), and **large language model reasoning** (Groq LLaMA 3.3 70B) into a seamless pipeline wrapped in a modern dark-themed web interface built with Reflex.

> Try it live → [**Hugging Face Spaces**](https://huggingface.co/spaces/ayushsainime/socratic_maths_tutor.ai)

---

## Architecture

<div align="center">
  <img src="https://huggingface.co/datasets/ayushsainime/socratic_maths_tutor_media/resolve/main/architechrute%20diagram%20101.png" alt="Architecture Diagram" width="100%" />
</div>

| Layer | File(s) | Responsibility |
|-------|---------|----------------|
| **Frontend** | `tutor_app/ui.py` | Dark glassmorphism UI with upload, results, and chat panels |
| **State Management** | `tutor_app/state.py` | Reflex state orchestrating the 4-stage analysis pipeline |
| **Upload** | `backend/services/upload_service.py` | Saves uploaded images via Reflex's upload directory |
| **Math OCR** | `backend/services/math_ocr_service.py` | Pix2TeX model converts images → LaTeX |
| **Symbolic Analysis** | `backend/services/math_service.py` | SymPy parses LaTeX, classifies problem type, verifies symbolically |
| **AI Tutor** | `backend/services/tutor_service.py` | Sends Socratic prompts to Groq LLaMA 3.3 70B |
| **REST API** | `backend/api.py` | FastAPI endpoint exposing the pipeline programmatically |

---

## Features

- **Image Upload & OCR** — Snap a photo of handwritten math; the app extracts LaTeX using a vision-to-LaTeX neural network (Pix2TeX).
- **Symbolic Math Analysis** — Extracted expressions are parsed with SymPy for classification (Algebra, Calculus, Trigonometry, etc.), structural summarization, and symbolic verification.
- **Socratic AI Tutoring** — The AI never solves the problem. It asks exactly one guiding question per response, nudging the student forward.
- **Interactive Chat** — Continue the conversation with the tutor, which maintains full context of the problem and chat history.
- **Professional Dark UI** — Glassmorphism dark theme with a black, white & red accent palette, built with Reflex.
- **Privacy-First** — All processing happens server-side; no third-party data storage.
- **Docker-Ready** — Single-command containerized deployment.

---

## Tech Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Web Framework** | [Reflex](https://reflex.dev) v0.8.27 | Full-stack Python framework with React frontend |
| **AI / LLM** | [Groq](https://groq.com) — LLaMA 3.3 70B | Fast inference for Socratic tutoring prompts |
| **Math OCR** | [Pix2TeX](https://github.com/lukas-blecher/LaTeX-OCR) | Deep learning image → LaTeX conversion |
| **Symbolic Math** | [SymPy](https://www.sympy.org) | LaTeX parsing, classification, simplification & solving |
| **REST API** | [FastAPI](https://fastapi.tiangolo.com) | Programmatic access endpoint |
| **Containerization** | [Docker](https://www.docker.com) | Production deployment |

---

## Quick Start

### Prerequisites

- **Python 3.11+**
- **Groq API Key** — Get one free at [console.groq.com](https://console.groq.com)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/ayushsainime/SOCRATIC_MATH_TUTOR.AI.git
cd SOCRATIC_MATH_TUTOR.AI

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your API key
echo GROQ_API_KEY=your_key_here > .env

# 5. Run the application
reflex run
```

The app will be live at **http://localhost:3000**

---

## Docker Deployment

```bash
# Build the image
docker build -t socratic-maths-tutor .

# Run the container
docker run -d \
  --name socratic-tutor \
  -p 7860:7860 \
  -e GROQ_API_KEY=your_groq_api_key \
  socratic-maths-tutor
```

Access at **http://localhost:7860**

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ | Your Groq API key for LLM inference |

---

## Project Structure

```
Socratic Maths Tutor
├── tutor_app/                  # Frontend (Reflex)
│   ├── tutor_app.py            # App entry point
│   ├── ui.py                   # UI components & layout
│   ├── state.py                # State management & event handlers
│   └── constants.py            # App configuration constants
│
├── backend/                    # Backend services
│   ├── api.py                  # FastAPI REST endpoint
│   ├── models.py               # Pydantic response models
│   └── services/
│       ├── upload_service.py   # File upload handling
│       ├── math_ocr_service.py # Pix2TeX LaTeX OCR
│       ├── math_service.py     # SymPy symbolic analysis
│       └── tutor_service.py    # Groq Socratic prompting
│
├── models/pix2tex/             # OCR model weights
├── Dockerfile                  # Production container
├── requirements.txt            # Python dependencies
└── rxconfig.py                 # Reflex configuration
```

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. **Fork** the repository
2. Create a **feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. Open a **Pull Request**

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ for mathematics education</sub>
  <br/><br/>
  <strong>Made by Ayush Saini</strong>
  <br/>
  <a href="https://www.linkedin.com/in/ayush-saini-30a4a0372/">
    <img src="https://img.shields.io/badge/LinkedIn-Ayush%20Saini-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
</div>
