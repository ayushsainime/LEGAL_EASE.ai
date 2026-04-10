---
title: Socratic Maths Tutor AI
emoji: 🎓
colorFrom: red
colorTo: gray
sdk: docker
app_port: 3000
pinned: false
license: mit
short_description: Socratic AI-powered mathematics tutoring with image OCR
---

<p align="center">
  <img src="https://huggingface.co/datasets/ayushsainime/socratic_maths_tutor_media/resolve/main/female-math-tutor-writes-equations-blackboard-chalk-student-writes-them-down-notebook-vector-413658303.jpg" alt="Socratic Maths Tutor" width="120" height="120" style="border-radius: 20px; border: 3px solid #E63946;" />
</p>

<h1 align="center">SOCRATIC MATHS TUTOR</h1>

<p align="center">
  <em>Socratic AI-Powered Mathematics Tutoring</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Reflex-0.8.27-00B4D8?style=for-the-badge&logo=react&logoColor=white" alt="Reflex" />
  <img src="https://img.shields.io/badge/Groq-LLaMA_3.3-F55036?style=for-the-badge&logoColor=white" alt="Groq" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-demo">Demo</a> •
  <a href="#%EF%B8%8F-architecture">Architecture</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#-docker-deployment">Docker</a>
</p>

---

## ✨ Features

- **📷 Image Upload & OCR** — Snap a photo of handwritten math and the app extracts LaTeX using a deep-learning OCR model (Pix2TeX)
- **🧠 Symbolic Math Analysis** — Parsed expressions are analyzed with SymPy for structure classification, variable detection, and symbolic verification
- **🎓 Socratic AI Tutoring** — Instead of giving away answers, the AI asks one guiding question at a time using the Socratic method (powered by Groq's LLaMA 3.3 70B)
- **💬 Interactive Chat** — Follow-up conversation with the tutor that keeps guiding you step by step
- **🌙 Professional Dark UI** — Glassmorphism dark theme with a black, white & red accent palette built with Reflex
- **🔒 Privacy-First** — All processing happens locally; no third-party data storage
- **🐳 Docker-Ready** — One-command deployment with the included Dockerfile

---

## 🎥 Demo

1. **Upload** a photo of your handwritten math equation
2. **Analyze** — The app reads the math, classifies the problem type, verifies symbolically
3. **Get a guiding question** — The AI tutor responds with one Socratic question
4. **Chat** — Ask follow-ups and the tutor keeps guiding you without ever giving the answer away

---

## 🏗️ Architecture

```
Socratic Maths Tutor
├── tutor_app/                  # Frontend (Reflex)
│   ├── ui.py                   # UI components & layout
│   ├── state.py                # App state & event handlers
│   ├── constants.py            # App config constants
│   └── tutor_app.py            # Reflex app entry point
│
├── backend/                    # Backend services
│   ├── api.py                  # FastAPI REST endpoints
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

## ⚡ Quick Start

### Prerequisites

- **Python 3.11+**
- **Groq API Key** — Get one free at [console.groq.com](https://console.groq.com)

### 1. Clone the Repository

```bash
git clone https://github.com/ayushsainime/SOCRATIC_MATH_TUTOR.AI.git
cd SOCRATIC_MATH_TUTOR.AI
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Your Groq API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the App

```bash
reflex run
```

The app will be live at **http://localhost:3000** 🚀

---

## 🧰 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | [Reflex](https://reflex.dev) (v0.8.27) | Full-stack Python web framework with React under the hood |
| **AI / LLM** | [Groq](https://groq.com) — LLaMA 3.3 70B | Fast inference for Socratic tutoring prompts |
| **Math OCR** | [Pix2TeX](https://github.com/lukas-blecher/LaTeX-OCR) | Deep learning image → LaTeX conversion |
| **Symbolic Math** | [SymPy](https://www.sympy.org) | LaTeX parsing, classification, simplification & solving |
| **Backend API** | [FastAPI](https://fastapi.tiangolo.com) | REST endpoint for programmatic access |
| **Deployment** | Docker | Containerized production deployment |

---

## 🔬 How It Works

The application follows a 4-stage pipeline:

### Stage 1: Image Upload & LaTeX Extraction
The uploaded image is processed by **Pix2TeX**, a vision-to-LaTeX neural network that converts handwritten math notation into structured LaTeX code.

### Stage 2: Symbolic Math Analysis
The extracted LaTeX is parsed by **SymPy's LaTeX parser** into a symbolic expression tree. The system then:
- **Classifies** the problem type (Algebra, Calculus, Trigonometry, etc.)
- **Summarizes** the expression structure (root node, detected variables)
- **Verifies** the expression symbolically (simplification, identity checking, equation solving)

### Stage 3: Socratic AI Response
The math context (extracted LaTeX, problem type, structure, verification) is sent to **Groq's LLaMA 3.3 70B** model with a carefully crafted Socratic prompt. The AI is instructed to **never solve the problem** — instead it asks exactly one guiding question that nudges the student forward.

### Stage 4: Interactive Follow-up
Students can continue the conversation via the chat panel. The tutor maintains full context of the math problem and chat history, responding with concise Socratic guidance (2–4 sentences ending with a question).

---

## 🐳 Docker Deployment

Build and run with Docker:

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

## 🎨 UI Design

The interface features a **dark glassmorphism** theme:

- **Background**: Dark abstract wallpaper with full-viewport cover
- **Cards**: Semi-transparent dark panels with backdrop blur (`rgba(15, 15, 18, 0.92)`)
- **Accent Color**: `#E63946` — a bold red used for buttons, highlights, and interactive elements
- **Typography**: [Quicksand](https://fonts.google.com/specimen/Quicksand) — clean, modern, and highly readable
- **Chat Bubbles**: Tutor messages in red-tinted glass, user messages in neutral glass
- **Responsive**: Two-column layout that wraps gracefully on smaller screens

---

## 📁 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ | Your Groq API key for LLM inference |

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. Create a **feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. Open a **Pull Request**

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ for mathematics education
</p>