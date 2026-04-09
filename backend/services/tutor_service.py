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


def ask_socratic_question(
    extracted_text: str,
    problem_type: str,
    structure_summary: str,
    verification_summary: str,
) -> str:
    """Send math context to Groq using a Socratic prompt."""
    system_prompt = (
        "You are a Socratic tutor for handwritten math. "
        f"The extracted math is: {extracted_text}. "
        f"The detected problem type is: {problem_type}. "
        f"The structural analysis is: {structure_summary}. "
        f"The symbolic verification summary is: {verification_summary}. "
        "DO NOT solve the problem for the student. "
        "Ask exactly one short guiding question that helps them inspect their work, "
        "spot a likely mistake, or choose the next step."
    )

    try:
        client = get_groq_client()
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Ask one guiding question."},
            ],
        )
        return completion.choices[0].message.content or "No response was returned."
    except Exception as error:
        raise RuntimeError(f"Groq request failed: {error}") from error


def ask_followup_question(
    extracted_text: str,
    problem_type: str,
    structure_summary: str,
    verification_summary: str,
    chat_history: list[dict],
    user_question: str,
) -> str:
    """Continue a Socratic conversation about the math problem."""
    system_prompt = (
        "You are a Socratic tutor for handwritten math. "
        "You guide students through problems by asking probing questions and never giving away answers. "
        f"The extracted math is: {extracted_text}. "
        f"The detected problem type is: {problem_type}. "
        f"The structural analysis is: {structure_summary}. "
        f"The symbolic verification summary is: {verification_summary}. "
        "Keep your responses concise (2-4 sentences). "
        "Always end with a guiding question that nudges the student forward."
    )

    messages = [{"role": "system", "content": system_prompt}]
    for msg in chat_history:
        role = "assistant" if msg["role"] == "tutor" else "user"
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
        raise RuntimeError(f"Groq request failed: {error}") from error
