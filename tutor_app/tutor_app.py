from __future__ import annotations

import os
import time
from pathlib import Path

import easyocr
from groq import Groq
import reflex as rx
import torch

UPLOAD_ID = "math_upload"
DEFAULT_MESSAGE = (
    "Upload an image of your math work, then click Analyze Image to get one "
    "guiding Socratic question."
)

_ocr_reader: easyocr.Reader | None = None
_groq_client: Groq | None = None


def get_ocr_reader() -> easyocr.Reader:
    """Create the OCR reader once and reuse it."""
    global _ocr_reader

    if _ocr_reader is None:
        _ocr_reader = easyocr.Reader(["en"], gpu=torch.cuda.is_available())

    return _ocr_reader


def get_groq_client() -> Groq:
    """Create the Groq client once and reuse it."""
    global _groq_client

    if _groq_client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("Set the GROQ_API_KEY environment variable first.")
        _groq_client = Groq(api_key=api_key)

    return _groq_client


async def save_uploaded_file(upload_file) -> Path:
    """Save the uploaded image into Reflex's upload directory."""
    upload_dir = rx.get_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)

    original_name = Path(upload_file.filename or "math_homework.png").name
    saved_name = f"{int(time.time())}_{original_name}"
    saved_path = upload_dir / saved_name

    file_bytes = await upload_file.read()
    saved_path.write_bytes(file_bytes)
    return saved_path


def extract_text_from_image(image_path: Path) -> str:
    """Run EasyOCR on the saved image."""
    try:
        reader = get_ocr_reader()
        chunks = reader.readtext(str(image_path), detail=0, paragraph=True)
        extracted_text = " ".join(chunks).strip()

        if not extracted_text:
            raise RuntimeError("No readable text was found in the image.")

        return extracted_text
    except Exception as error:
        raise RuntimeError(f"OCR failed: {error}") from error


def ask_socratic_question(extracted_text: str) -> str:
    """Send the OCR output to Groq using a strict Socratic prompt."""
    system_prompt = (
        "You are a Socratic tutor. The user has uploaded an image of their work. "
        f"Here is the extracted text: {extracted_text}. "
        "DO NOT solve the problem for them. Ask a single guiding question to help "
        "them find their mistake or figure out the next step."
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


class TutorState(rx.State):
    """State for the Socratic AI Tutor."""

    uploaded_image_url: str = ""
    extracted_text: str = ""
    tutor_response: str = DEFAULT_MESSAGE
    error_message: str = ""
    is_loading: bool = False

    async def analyze_image(self, files: list) -> None:
        """Save the image, extract text, and ask the tutor for one hint."""
        self.is_loading = True
        self.error_message = ""
        self.extracted_text = ""
        self.tutor_response = DEFAULT_MESSAGE

        try:
            if not files:
                raise RuntimeError("Please upload an image before analyzing it.")

            saved_path = await save_uploaded_file(files[0])
            self.uploaded_image_url = rx.get_upload_url(saved_path.name)
            self.extracted_text = extract_text_from_image(saved_path)
            self.tutor_response = ask_socratic_question(self.extracted_text)
        except Exception as error:
            self.error_message = str(error)
            self.tutor_response = "I couldn't analyze that image yet. Try a clearer photo."
        finally:
            self.is_loading = False


def upload_box() -> rx.Component:
    return rx.upload(
        rx.vstack(
            rx.text("Drag an image here or click to browse.", font_weight="600"),
            rx.text("PNG, JPG, JPEG, or WEBP", color="#64748b", font_size="0.95em"),
            spacing="2",
            align="center",
        ),
        id=UPLOAD_ID,
        accept={"image/*": [".png", ".jpg", ".jpeg", ".webp"]},
        max_files=1,
        border="2px dashed #94a3b8",
        border_radius="16px",
        padding="2.5em",
        width="100%",
        bg="white",
    )


def response_box() -> rx.Component:
    return rx.box(
        rx.heading("Tutor Response", size="5"),
        rx.text(
            TutorState.tutor_response,
            white_space="pre-wrap",
            line_height="1.7",
        ),
        width="100%",
        padding="1.25em",
        border_radius="16px",
        bg="white",
        box_shadow="0 10px 30px rgba(15, 23, 42, 0.08)",
    )


def extracted_text_box() -> rx.Component:
    return rx.cond(
        TutorState.extracted_text != "",
        rx.box(
            rx.heading("Extracted Text", size="4"),
            rx.text(
                TutorState.extracted_text,
                white_space="pre-wrap",
                color="#334155",
            ),
            width="100%",
            padding="1.25em",
            border_radius="16px",
            bg="#f8fafc",
            border="1px solid #e2e8f0",
        ),
    )


def image_preview() -> rx.Component:
    return rx.cond(
        TutorState.uploaded_image_url != "",
        rx.image(
            src=TutorState.uploaded_image_url,
            alt="Uploaded homework image",
            max_height="260px",
            border_radius="16px",
            object_fit="contain",
            border="1px solid #e2e8f0",
            bg="white",
            padding="0.5em",
        ),
    )


def error_text() -> rx.Component:
    return rx.cond(
        TutorState.error_message != "",
        rx.text(
            TutorState.error_message,
            color="#b91c1c",
            font_weight="600",
            text_align="center",
        ),
    )


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Socratic AI Tutor", size="8"),
            rx.text(
                "Upload a photo of your math homework or code. The app reads the "
                "image with OCR and replies with one guiding question instead of "
                "the final answer.",
                text_align="center",
                color="#475569",
                max_width="42em",
            ),
            upload_box(),
            rx.vstack(
                rx.foreach(
                    rx.selected_files(UPLOAD_ID),
                    lambda file_name: rx.text(file_name, color="#475569"),
                ),
                width="100%",
                align="start",
            ),
            rx.button(
                "Analyze Image",
                on_click=TutorState.analyze_image(rx.upload_files(UPLOAD_ID)),
                loading=TutorState.is_loading,
                size="3",
                width="100%",
                color_scheme="blue",
            ),
            error_text(),
            image_preview(),
            response_box(),
            extracted_text_box(),
            spacing="5",
            align="center",
            width="100%",
            max_width="48em",
            padding="2em",
        ),
        min_height="100vh",
        width="100%",
        bg="#eef4ff",
    )


app = rx.App()
app.add_page(index, title="Socratic AI Tutor")
