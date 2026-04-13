<!-- ---
title: Legal Ease AI
emoji: ⚖️
colorFrom: yellow
colorTo: amber
sdk: docker
app_port: 7860
pinned: false
---
 -->
<div align="center">

<img src="https://huggingface.co/datasets/ayushsainime/legal_ease_media/resolve/main/law-concept-there-are-many-books-and-scales-of-justice-in-cartoon-style-for-your-design-vector.jpg" width="140" height="140" style="border-radius: 20px; border: 3px solid #F29F05; box-shadow: 0 0 28px rgba(242, 159, 5, 0.4);">

<br/>
<br/>

# ⚖️ Legal Ease AI

### *AI-Powered Legal Document Simplifier & Intelligent Chat*

**Transform complex legal jargon into plain English. Ask questions. Get instant clarity.**

<br/>

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Try_Now-FF4B4B?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co/spaces/ayushsainime/Legal_ease.ai)
[![YouTube](https://img.shields.io/badge/📺_Watch_Demo-Video-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtube.com)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ayushsainime/SOCRATIC_MATH_TUTOR.AI)

<br/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Reflex](https://img.shields.io/badge/Reflex-0.8.27-6E40C9?style=flat-square&logo=reflex&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-F55036?style=flat-square&logo=groq&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)
![PyMuPDF](https://img.shields.io/badge/PyMuPDF-PDF_Extraction-4A90D9?style=flat-square&logo=adobeacrobatreader&logoColor=white)
![python-docx](https://img.shields.io/badge/python--docx-DOCX_Parsing-2E86C1?style=flat-square&logo=microsoftword&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker&logoColor=white)
![HF Spaces](https://img.shields.io/badge/HF_Spaces-Deployed-FFD21E?style=flat-square&logo=huggingface&logoColor=black)

</div>

---

## 🎯 Overview

**Legal Ease AI** is a state-of-the-art web application that empowers anyone to **understand legal documents instantly**. Simply upload a PDF, DOCX, or TXT file, and our AI will:

- ✨ **Simplify** complex legal language into clear, plain English
- 💬 **Chat** — Ask follow-up questions about any clause, term, or section
- 📋 **Analyze** — Get document metadata, key takeaways, and clause highlights
- 🔍 **Explore** — View the original extracted text side-by-side

No legal background needed. Just upload and understand.

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 📄 Multi-Format Support
Upload **PDF**, **DOCX**, or **TXT** files — we handle the rest with seamless text extraction powered by PyMuPDF and python-docx.

</td>
<td width="50%">

### 🔄 Legal Simplification
Our AI rewrites complex legal jargon into **clear, everyday English** while preserving the original meaning, obligations, and rights accurately.

</td>
</tr>
<tr>
<td width="50%">

### 💬 Intelligent Document Chat
Ask questions about your document in natural language. Get **instant, accurate answers** grounded in the document's actual content.

</td>
<td width="50%">

### 📋 Document Metadata
Instantly see file name, document type, page count, and word count — a quick overview before you dive into the details.

</td>
</tr>
<tr>
<td width="50%">

### 🔍 Raw Text Viewer
Expand a collapsible section to view the **original extracted text** — full transparency into what the AI is analyzing.

</td>
<td width="50%">

### 📝 Sample Documents
Not ready with a file? Try our **built-in sample legal agreements** to see how the app works before uploading your own documents.

</td>
</tr>
<tr>
<td width="50%">

### ⚡ Lightning-Fast AI
Powered by **Groq's LPU inference engine** with Llama 3.3 70B — get responses in seconds, not minutes.

</td>
<td width="50%">

### 🎨 Premium Dark UI
Sleek **glassmorphism design** with golden amber accents — a professional, modern interface that's easy on the eyes.

</td>
</tr>
</table>

---

## 🏗️ Architecture

<div align="center">

<img src="https://huggingface.co/datasets/ayushsainime/legal_ease_media/resolve/main/legal_ease_architechture.png" width="800" alt="Legal Ease AI Architecture Diagram">

</div>

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Frontend Framework** | [Reflex](https://reflex.dev/) (Python-based reactive UI) |
| **AI Engine** | [Groq](https://groq.com/) — Llama 3.3 70B Versatile |
| **PDF Extraction** | [PyMuPDF](https://pymupdf.readthedocs.io/) |
| **DOCX Extraction** | [python-docx](https://python-docx.readthedocs.io/) |
| **Backend** | Python / FastAPI |
| **Deployment** | Docker on Hugging Face Spaces |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- A [Groq API key](https://console.groq.com/) (free tier available)

### Installation

```bash
# Clone the repository
git clone https://github.com/ayushsainime/SOCRATIC_MATH_TUTOR.AI.git
cd SOCRATIC_MATH_TUTOR.AI

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Set your API key
echo "GROQ_API_KEY=your_key_here" > .env

# Launch the app
reflex run
```

The app will be available at `http://localhost:3000`.

---

## 🐳 Docker Deployment

### Local

```bash
docker build -t legal-ease-ai .
docker run -p 7860:7860 -e GROQ_API_KEY=your_key legal-ease-ai
```

### Hugging Face Spaces

1. Create a new **Docker Space** on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Push this repository to the Space
3. Add `GROQ_API_KEY` as a **Repository Secret** in Space Settings
4. Your app goes live automatically! 🎉

---

## 🎮 How It Works

1. **Upload** — Drag & drop or browse to upload a legal document (PDF, DOCX, or TXT)
2. **Extract** — Text is extracted using PyMuPDF (PDF) or python-docx (DOCX)
3. **Simplify** — Groq's Llama 3.3 70B rewrites the document in plain, understandable English
4. **Chat** — Ask follow-up questions about any clause, term, or section — answers are grounded in the document content

---

## ⚠️ Disclaimer

> **This tool is for informational and educational purposes only.** It does **not** constitute legal advice and should not be relied upon as a substitute for professional legal counsel. Always consult a qualified attorney for legal matters.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute.

---

<div align="center">

<br/>

**Built with ❤️ by [Ayush Saini](https://www.linkedin.com/in/ayush-saini-30a4a0372/)**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ayush-saini-30a4a0372/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ayushsainime)

<br/>

⭐ **If you found this project helpful, please give it a star!** ⭐

</div>