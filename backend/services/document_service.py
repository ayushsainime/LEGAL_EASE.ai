from __future__ import annotations

from pathlib import Path
from typing import Any


def extract_text_from_pdf(file_path: Path) -> str:
    """Extract text from a PDF file using PyMuPDF."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise RuntimeError(
            "PyMuPDF is not installed. Install it with: pip install PyMuPDF"
        )

    doc = fitz.open(str(file_path))
    pages: list[str] = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        if text:
            pages.append(f"--- Page {page_num} ---\n{text}")

    doc.close()

    if not pages:
        raise RuntimeError(
            "No text could be extracted from the PDF. "
            "It may be a scanned document — try uploading a text-based PDF."
        )

    return "\n\n".join(pages)


def extract_text_from_docx(file_path: Path) -> str:
    """Extract text from a DOCX file."""
    try:
        from docx import Document
    except ImportError:
        raise RuntimeError(
            "python-docx is not installed. Install it with: pip install python-docx"
        )

    doc = Document(str(file_path))
    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]

    if not paragraphs:
        raise RuntimeError("No text could be extracted from the DOCX file.")

    return "\n\n".join(paragraphs)


def extract_text_from_txt(file_path: Path) -> str:
    """Read plain text from a TXT file."""
    text = file_path.read_text(encoding="utf-8", errors="replace").strip()

    if not text:
        raise RuntimeError("The text file appears to be empty.")

    return text


def extract_text(file_path: Path) -> str:
    """Route to the correct extractor based on file extension."""
    suffix = file_path.suffix.lower()

    extractors = {
        ".pdf": extract_text_from_pdf,
        ".docx": extract_text_from_docx,
        ".doc": extract_text_from_docx,
        ".txt": extract_text_from_txt,
    }

    extractor = extractors.get(suffix)

    if extractor is None:
        supported = ", ".join(extractors.keys())
        raise RuntimeError(
            f"Unsupported file type '{suffix}'. Supported types: {supported}"
        )

    return extractor(file_path)


def get_document_metadata(file_path: Path, extracted_text: str) -> dict[str, Any]:
    """Return lightweight metadata about the uploaded document."""
    suffix = file_path.suffix.lower()
    word_count = len(extracted_text.split())
    char_count = len(extracted_text)

    doc_type_map = {
        ".pdf": "PDF Document",
        ".docx": "Word Document",
        ".doc": "Word Document",
        ".txt": "Plain Text",
    }

    page_count = 1
    if suffix == ".pdf":
        try:
            import fitz

            doc = fitz.open(str(file_path))
            page_count = len(doc)
            doc.close()
        except Exception:
            page_count = 1

    return {
        "file_name": file_path.name,
        "file_type": doc_type_map.get(suffix, "Unknown"),
        "page_count": page_count,
        "word_count": word_count,
        "char_count": char_count,
    }