---
title: Legal Doc AI
emoji: ⚖️
colorFrom: yellow
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

# ⚖️ Legal Doc AI — AI-Powered Legal Document Simplifier & Chat

A web application that simplifies legal documents into plain English and lets you chat with them. Upload PDFs, DOCX files, or text documents, get an easy-to-understand version, and ask questions about any clause or term.

**Built with** [Reflex](https://reflex.dev/) · [Groq](https://groq.com/) · [PyMuPDF](https://pymupdf.readthedocs.io/) · [python-docx](https://python-docx.readthedocs.io/)

---

## ✨ Features

- **📄 Multi-format support** — Upload PDF, DOCX, or TXT files
- **🔄 Legal simplification** — Complex legal jargon rewritten in plain English
- **💬 Chat with your document** — Ask questions and get answers grounded in the document's content
- **📋 Document metadata** — File name, type, page count, and word count at a glance
- **🔍 Raw text viewer** — Expandable section to see the original extracted text
- **📝 Sample documents** — Try built-in sample legal agreements to see how it works
- **🎨 Dark glassmorphism UI** — Sleek, modern interface with a golden amber accent
- **⚡ Fast AI responses** — Powered by Groq's LPU inference engine (Llama 3.3 70B)
- **🔒 Privacy-first** — Documents are processed server-side; no third-party data storage

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- A [Groq API key](https://console.groq.com/)

### Installation

```bash
# Clone the repo
git clone https://github.com/ayushsainime/SOCRATIC_MATH_TUTOR.AI.git
cd SOCRATIC_MATH_TUTOR.AI

# Install dependencies
pip install -r requirements.txt

# Set your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# Run the app
reflex run
```

The app will be available at `http://localhost:3000`.

---

## 🐳 Docker (Local)

```bash
# Build and run
docker build -t legal-doc-ai .
docker run -p 3000:3000 -e GROQ_API_KEY=your_key legal-doc-ai
```

---

## ☁️ Hugging Face Spaces Deployment

This app is configured for HF Spaces Docker deployment:

1. Create a new **Docker** Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Push this repo to the Space's Git repository
3. Add `GROQ_API_KEY` as a **Repository Secret** in Space Settings → Variables and secrets
4. The Space will build and deploy automatically

---

## 📁 Project Structure

```
├── tutor_app/                 # Frontend (Reflex)
│   ├── tutor_app.py           # App entry point
│   ├── ui.py                  # All UI components
│   ├── state.py               # State management (LegalDocState)
│   └── constants.py           # App title, upload ID, defaults
├── backend/
│   └── services/
│       ├── document_service.py # Text extraction (PDF, DOCX, TXT)
│       ├── legal_service.py    # AI simplification, summarization, chat
│       └── upload_service.py   # File upload handling
├── .env                       # GROQ_API_KEY (gitignored)
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🛠️ How It Works

1. **Upload** — Drag & drop or browse to upload a legal document (PDF, DOCX, or TXT)
2. **Extract** — Text is extracted using PyMuPDF (PDF) or python-docx (DOCX)
3. **Simplify** — The Groq LLM rewrites the document in plain, understandable English
4. **Chat** — Ask follow-up questions about any clause, term, or section — answers are grounded in the document content

---

## ⚠️ Disclaimer

This tool is for **informational purposes only** and does **not** constitute legal advice. Always consult a qualified attorney for legal matters.

---

## 📝 License

MIT License — feel free to use and modify.

---

Made by [Ayush Saini](https://www.linkedin.com/in/ayush-saini-30a4a0372/)