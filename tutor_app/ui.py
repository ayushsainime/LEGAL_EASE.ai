from __future__ import annotations

import reflex as rx

from tutor_app.constants import APP_TITLE, UPLOAD_ID
from tutor_app.state import TutorState


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
            rx.heading("Extracted Math (LaTeX)", size="4"),
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


def math_analysis_box() -> rx.Component:
    return rx.cond(
        TutorState.problem_type != "",
        rx.box(
            rx.heading("Math Analysis", size="4"),
            rx.text(f"Problem Type: {TutorState.problem_type}", font_weight="600"),
            rx.text(
                f"Structure: {TutorState.structure_summary}",
                white_space="pre-wrap",
                color="#334155",
            ),
            rx.text(
                f"Verification: {TutorState.verification_summary}",
                white_space="pre-wrap",
                color="#334155",
            ),
            rx.text(
                f"Normalized Expression: {TutorState.normalized_expression}",
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
            rx.heading(APP_TITLE, size="8"),
            rx.text(
                "Upload a photo of a handwritten math equation or worked solution. "
                "The app reads the math, analyzes its structure, checks it "
                "symbolically, and replies with one guiding question instead of "
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
            math_analysis_box(),
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
