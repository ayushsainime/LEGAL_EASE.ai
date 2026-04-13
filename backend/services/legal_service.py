from __future__ import annotations

import os
from pathlib import Path

from groq import Groq

_groq_client: Groq | None = None


def _read_key_from_dotenv() -> str | None:
    """Read GROQ_API_KEY from project .env when env var is not exported."""
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        return None

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == "GROQ_API_KEY":
            return value.strip().strip('"').strip("'")
    return None


def get_groq_client() -> Groq:
    """Create the Groq client once and reuse it."""
    global _groq_client

    if _groq_client is None:
        api_key = os.getenv("GROQ_API_KEY") or _read_key_from_dotenv()
        if not api_key:
            raise RuntimeError("Set the GROQ_API_KEY environment variable first.")
        _groq_client = Groq(api_key=api_key)

    return _groq_client


# ─── System prompts ────────────────────────────────────────────────

SIMPLIFY_SYSTEM_PROMPT = (
    "You are a legal document simplifier. Your job is to take legal text and "
    "rewrite it in clear, plain English that anyone can understand.\n\n"
    "Rules:\n"
    "- Replace legal jargon with everyday language.\n"
    "- Break down complex sentences into shorter, simpler ones.\n"
    "- Preserve the original meaning accurately — do not add or remove obligations, rights, or facts.\n"
    "- Use bullet points or numbered lists where it improves readability.\n"
    "- If there are important clauses (e.g., termination, liability, confidentiality), highlight them.\n"
    "- At the end, provide a brief 'Key Takeaways' section with the most important points.\n"
    "- If the document is very long, organize the simplification by sections matching the original."
)

SUMMARIZE_SYSTEM_PROMPT = (
    "You are a legal document summarizer. Provide a concise summary of the legal document.\n\n"
    "Your summary should:\n"
    "- Identify the type of document (contract, agreement, notice, etc.).\n"
    "- List the main parties involved.\n"
    "- State the key obligations, rights, and terms.\n"
    "- Flag any notable clauses (penalties, termination conditions, deadlines).\n"
    "- Be thorough but concise — aim for 3-6 paragraphs.\n"
    "- Use plain English, not legal jargon."
)

CHAT_SYSTEM_PROMPT = (
    "You are a helpful legal document assistant. The user has uploaded a legal document "
    "and you help them understand it by answering their questions.\n\n"
    "Rules:\n"
    "- Answer based ONLY on the content of the provided document.\n"
    "- If the user asks something not covered in the document, say so honestly.\n"
    "- Explain legal terms in plain language when they appear.\n"
    "- Reference specific sections or clauses when relevant.\n"
    "- Be concise but thorough — aim for 2-5 sentences unless more detail is needed.\n"
    "- Do NOT provide legal advice — you are an informational assistant, not a lawyer.\n"
    "- Add a disclaimer if the user seems to be seeking binding legal advice."
)


# ─── Public API ────────────────────────────────────────────────────

def simplify_document(extracted_text: str) -> str:
    """Send document text to Groq and get a plain-English simplification."""
    # Truncate very long documents to fit context window
    max_chars = 30000
    text = extracted_text[:max_chars]
    if len(extracted_text) > max_chars:
        text += "\n\n[... Document truncated due to length ...]"

    try:
        client = get_groq_client()
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SIMPLIFY_SYSTEM_PROMPT},
                {"role": "user", "content": f"Please simplify this legal document in plain English:\n\n{text}"},
            ],
        )
        return completion.choices[0].message.content or "No simplification was returned."
    except Exception as error:
        raise RuntimeError(f"Simplification failed: {error}") from error


def summarize_document(extracted_text: str) -> str:
    """Send document text to Groq and get a concise summary."""
    max_chars = 30000
    text = extracted_text[:max_chars]
    if len(extracted_text) > max_chars:
        text += "\n\n[... Document truncated due to length ...]"

    try:
        client = get_groq_client()
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SUMMARIZE_SYSTEM_PROMPT},
                {"role": "user", "content": f"Please summarize this legal document:\n\n{text}"},
            ],
        )
        return completion.choices[0].message.content or "No summary was returned."
    except Exception as error:
        raise RuntimeError(f"Summarization failed: {error}") from error


def chat_with_document(
    extracted_text: str,
    chat_history: list[dict],
    user_question: str,
) -> str:
    """Answer a user's question about the uploaded legal document."""
    max_chars = 30000
    text = extracted_text[:max_chars]
    if len(extracted_text) > max_chars:
        text += "\n\n[... Document truncated due to length ...]"

    system_prompt = (
        CHAT_SYSTEM_PROMPT
        + f"\n\n--- DOCUMENT CONTENT ---\n{text}\n--- END OF DOCUMENT ---"
    )

    messages = [{"role": "system", "content": system_prompt}]
    for msg in chat_history:
        role = "assistant" if msg["role"] == "assistant" else "user"
        messages.append({"role": role, "content": msg["content"]})

    messages.append({"role": "user", "content": user_question})

    try:
        client = get_groq_client()
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
        )
        return completion.choices[0].message.content or "No response was returned."
    except Exception as error:
        raise RuntimeError(f"Chat request failed: {error}") from error