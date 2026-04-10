from __future__ import annotations

import reflex as rx

from tutor_app.constants import APP_TITLE, UPLOAD_ID
from tutor_app.state import TutorState, ChatMessage

# ─── Theme constants ───────────────────────────────────────────────
BG_IMAGE = (
    "https://huggingface.co/datasets/ayushsainime/socratic_maths_tutor_media/"
    "resolve/main/istockphoto-2162577218-2048x2048.jpg"
)
HEADING_IMAGE = (
    "https://huggingface.co/datasets/ayushsainime/socratic_maths_tutor_media/"
    "resolve/main/female-math-tutor-writes-equations-blackboard-chalk-"
    "student-writes-them-down-notebook-vector-413658303.jpg"
)

ACCENT = "#E63946"
ACCENT_HOVER = "#FF4D5A"
DARK_BG = "rgba(10, 10, 10, 0.88)"
CARD_BG = "rgba(15, 15, 18, 0.92)"
CARD_BORDER = "rgba(255, 255, 255, 0.1)"
GLASS = "rgba(15, 15, 18, 0.85)"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "rgba(255, 255, 255, 0.7)"
TEXT_MUTED = "rgba(255, 255, 255, 0.5)"
INPUT_BG = "rgba(255, 255, 255, 0.08)"
INPUT_BORDER = "rgba(255, 255, 255, 0.15)"
TUTOR_BUBBLE = "rgba(230, 57, 70, 0.22)"
USER_BUBBLE = "rgba(255, 255, 255, 0.12)"
ERROR_RED = "#FF6B6B"
SUCCESS_GREEN = "rgba(76, 175, 80, 0.85)"


# ─── Reusable card wrapper ─────────────────────────────────────────
def _glass_card(*children, **kwargs) -> rx.Component:
    """Dark glassmorphism card used throughout the UI."""
    return rx.box(
        *children,
        background=CARD_BG,
        border=f"1px solid {CARD_BORDER}",
        border_radius="16px",
        backdrop_filter="blur(24px)",
        box_shadow="0 8px 32px rgba(0, 0, 0, 0.4)",
        padding=kwargs.get("padding", "1.5em"),
        width=kwargs.get("width", "100%"),
        **{k: v for k, v in kwargs.items()
           if k not in ("padding", "width")},
    )


# ─── Upload box ────────────────────────────────────────────────────
def upload_box() -> rx.Component:
    return rx.upload(
        rx.cond(
            TutorState.uploaded_image_name != "",
            rx.vstack(
                rx.image(
                    src=rx.get_upload_url(TutorState.uploaded_image_name),
                    alt="Uploaded homework image",
                    max_height="240px",
                    border_radius="12px",
                    object_fit="contain",
                    border=f"1px solid {ACCENT}",
                    bg="rgba(0,0,0,0.5)",
                    padding="0.5em",
                    box_shadow=f"0 0 16px rgba(230, 57, 70, 0.2)",
                ),
                rx.text(
                    "✅ Image uploaded — click to replace",
                    color="#4ADE80",
                    font_size="0.88em",
                    font_weight="600",
                ),
                spacing="2",
                align="center",
            ),
            rx.cond(
                rx.selected_files(UPLOAD_ID).length() > 0,
                rx.vstack(
                    rx.icon("file-check", size=36, color="#4ADE80"),
                    rx.text(
                        rx.selected_files(UPLOAD_ID)[0],
                        color=TEXT_PRIMARY,
                        font_weight="600",
                        font_size="0.95em",
                    ),
                    rx.text(
                        "File selected — click Analyze below",
                        color="#4ADE80",
                        font_size="0.85em",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.vstack(
                    rx.icon("image-plus", size=32, color=ACCENT),
                    rx.text(
                        "Drag an image here or click to browse",
                        font_weight="600",
                        color=TEXT_PRIMARY,
                        font_size="1em",
                    ),
                    rx.text(
                        "PNG · JPG · JPEG · WEBP",
                        color=TEXT_MUTED,
                        font_size="0.85em",
                    ),
                    spacing="3",
                    align="center",
                ),
            ),
        ),
        id=UPLOAD_ID,
        accept={"image/*": [".png", ".jpg", ".jpeg", ".webp"]},
        max_files=1,
        border=f"2px dashed rgba(230, 57, 70, 0.4)",
        border_radius="16px",
        padding="2.5em",
        width="100%",
        background=GLASS,
        _hover={"border_color": ACCENT},
        transition="border-color 0.3s ease",
    )


# ─── Tutor response card ──────────────────────────────────────────
def response_box() -> rx.Component:
    return _glass_card(
        rx.hstack(
            rx.icon("message-circle", size=20, color=ACCENT),
            rx.heading("Tutor Response", size="5", color=TEXT_PRIMARY),
            spacing="2",
            align="center",
        ),
        rx.box(
            rx.text(
                TutorState.tutor_response,
                white_space="pre-wrap",
                line_height="1.8",
                color="rgba(255, 255, 255, 0.88)",
                font_size="0.98em",
            ),
            margin_top="0.8em",
            padding_left="0.2em",
        ),
    )


# ─── Extracted LaTeX ──────────────────────────────────────────────
def extracted_text_box() -> rx.Component:
    return rx.cond(
        TutorState.extracted_text != "",
        _glass_card(
            rx.hstack(
                rx.icon("file-text", size=18, color=ACCENT),
                rx.heading("Extracted Math (LaTeX)", size="4", color=TEXT_PRIMARY),
                spacing="2",
                align="center",
            ),
            rx.text(
                TutorState.extracted_text,
                white_space="pre-wrap",
                color=TEXT_SECONDARY,
                margin_top="0.6em",
                font_family="monospace",
                font_size="0.92em",
            ),
            border_left=f"3px solid {ACCENT}",
        ),
    )


# ─── Math analysis card ───────────────────────────────────────────
def math_analysis_box() -> rx.Component:
    return rx.cond(
        TutorState.problem_type != "",
        _glass_card(
            rx.hstack(
                rx.icon("bar-chart-3", size=18, color=ACCENT),
                rx.heading("Math Analysis", size="4", color=TEXT_PRIMARY),
                spacing="2",
                align="center",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text("Problem Type:", font_weight="700", color=TEXT_PRIMARY, font_size="0.9em"),
                    rx.text(TutorState.problem_type, color=ACCENT, font_weight="600", font_size="0.9em"),
                    spacing="2",
                ),
                rx.box(
                    rx.text("Structure:", font_weight="700", color=TEXT_PRIMARY, font_size="0.85em"),
                    rx.text(
                        TutorState.structure_summary,
                        white_space="pre-wrap",
                        color=TEXT_SECONDARY,
                        font_size="0.85em",
                    ),
                ),
                rx.box(
                    rx.text("Verification:", font_weight="700", color=TEXT_PRIMARY, font_size="0.85em"),
                    rx.text(
                        TutorState.verification_summary,
                        white_space="pre-wrap",
                        color=TEXT_SECONDARY,
                        font_size="0.85em",
                    ),
                ),
                rx.box(
                    rx.text("Normalized:", font_weight="700", color=TEXT_PRIMARY, font_size="0.85em"),
                    rx.text(
                        TutorState.normalized_expression,
                        white_space="pre-wrap",
                        color=TEXT_SECONDARY,
                        font_family="monospace",
                        font_size="0.85em",
                    ),
                ),
                spacing="3",
                margin_top="0.6em",
                align="start",
                width="100%",
            ),
            border_left=f"3px solid {ACCENT}",
        ),
    )


# ─── Error text ────────────────────────────────────────────────────
def error_text() -> rx.Component:
    return rx.cond(
        TutorState.error_message != "",
        rx.hstack(
            rx.icon("circle-alert", size=18, color=ERROR_RED),
            rx.text(
                TutorState.error_message,
                color=ERROR_RED,
                font_weight="600",
                font_size="0.92em",
            ),
            spacing="2",
            justify="center",
            padding="0.6em",
            background="rgba(255, 107, 107, 0.08)",
            border_radius="10px",
            border=f"1px solid rgba(255, 107, 107, 0.2)",
            width="100%",
        ),
    )


# ─── Chat message bubble ──────────────────────────────────────────
def chat_message_bubble(msg: ChatMessage) -> rx.Component:
    is_tutor = msg.role == "tutor"
    return rx.box(
        rx.hstack(
            rx.cond(
                is_tutor,
                rx.box(
                    rx.icon("graduation-cap", size=16, color=ACCENT),
                    bg="rgba(230, 57, 70, 0.15)",
                    border_radius="8px",
                    padding="0.35em",
                    flex_shrink="0",
                ),
                rx.box(
                    rx.icon("user", size=16, color=TEXT_SECONDARY),
                    bg=USER_BUBBLE,
                    border_radius="8px",
                    padding="0.35em",
                    flex_shrink="0",
                ),
            ),
            rx.text(
                msg.content,
                white_space="pre-wrap",
                line_height="1.7",
                color="rgba(255, 255, 255, 0.9)",
                font_size="0.93em",
            ),
            spacing="3",
            align="start",
        ),
        padding="0.9em 1.1em",
        border_radius="14px",
        max_width="88%",
        align_self=rx.cond(is_tutor, "start", "end"),
        background=rx.cond(is_tutor, TUTOR_BUBBLE, USER_BUBBLE),
        border=rx.cond(
            is_tutor,
            f"1px solid rgba(230, 57, 70, 0.2)",
            f"1px solid {INPUT_BORDER}",
        ),
        margin_bottom="0.6em",
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.2)",
    )


# ─── Chat panel ───────────────────────────────────────────────────
def chat_box() -> rx.Component:
    return _glass_card(
        rx.hstack(
            rx.icon("messages-square", size=22, color=ACCENT),
            rx.heading("Conversation", size="6", color=TEXT_PRIMARY),
            spacing="2",
            align="center",
        ),
        rx.text(
            "Discuss your steps with the tutor. It will keep guiding you with Socratic questions.",
            color=TEXT_SECONDARY,
            margin_bottom="1em",
            font_size="0.9em",
        ),
        rx.cond(
            TutorState.extracted_text == "",
            rx.hstack(
                rx.icon("lock", size=14, color=TEXT_MUTED),
                rx.text(
                    "Upload and analyze an image first to start the conversation.",
                    color=TEXT_MUTED,
                    margin_bottom="1em",
                    font_size="0.88em",
                ),
                spacing="2",
            ),
        ),
        rx.box(
            rx.foreach(TutorState.chat_messages, chat_message_bubble),
            width="100%",
            min_height="420px",
            max_height="60vh",
            overflow_y="auto",
            padding="0.75em",
            border_radius="12px",
            background="rgba(0, 0, 0, 0.3)",
            border=f"1px solid {CARD_BORDER}",
            margin_bottom="1em",
            display="flex",
            flex_direction="column",
        ),
        rx.hstack(
            rx.input(
                placeholder="Ask a follow-up question...",
                value=TutorState.chat_input,
                on_change=TutorState.set_chat_input,
                flex="1",
                disabled=TutorState.extracted_text == "",
                background=INPUT_BG,
                border=f"1px solid {INPUT_BORDER}",
                color=TEXT_PRIMARY,
                _placeholder={"color": TEXT_MUTED},
                _focus={"border_color": ACCENT, "box_shadow": f"0 0 0 2px rgba(230, 57, 70, 0.2)"},
                border_radius="10px",
                padding="0.7em 1em",
                font_size="0.95em",
            ),
            rx.button(
                rx.hstack(
                    rx.icon("send", size=16),
                    rx.text("Send", font_weight="600"),
                    spacing="2",
                    align="center",
                ),
                on_click=TutorState.send_chat_message,
                loading=TutorState.is_chat_loading,
                disabled=TutorState.extracted_text == "",
                background=ACCENT,
                color="white",
                border="none",
                border_radius="10px",
                padding="0.7em 1.4em",
                font_weight="600",
                cursor="pointer",
                _hover={"background": ACCENT_HOVER, "transform": "translateY(-1px)"},
                transition="all 0.2s ease",
                box_shadow=f"0 4px 14px rgba(230, 57, 70, 0.3)",
            ),
            width="100%",
            spacing="3",
        ),
    )


# ─── Page heading ─────────────────────────────────────────────────
def _page_heading() -> rx.Component:
    return rx.hstack(
        rx.image(
            src=HEADING_IMAGE,
            height="180px",
            width="180px",
            border_radius="20px",
            object_fit="cover",
            border=f"3px solid {ACCENT}",
            box_shadow=f"0 0 32px rgba(230, 57, 70, 0.45)",
            flex_shrink="0",
        ),
        rx.vstack(
            rx.heading(
                APP_TITLE.upper(),
                size="8",
                color=TEXT_PRIMARY,
                font_weight="900",
                letter_spacing="0.06em",
                margin="0",
                padding="0",
                line_height="1",
            ),
            rx.text(
                "Socratic AI-Powered Mathematics Tutoring",
                color=ACCENT,
                font_size="0.92em",
                font_weight="500",
                letter_spacing="0.04em",
                margin="0",
                padding="0",
                margin_top="0.2em",
            ),
            rx.text(
                "Upload a photo of a handwritten math equation or worked solution. "
                "The app reads the math, analyzes its structure, checks it "
                "symbolically, and replies with one guiding question instead of the final answer.",
                color=TEXT_SECONDARY,
                font_size="0.85em",
                line_height="1.5",
                margin="0",
                padding="0",
                margin_top="0.4em",
                max_width="40em",
            ),
            spacing="0",
            align="start",
            padding="0",
            margin="0",
        ),
        spacing="5",
        align="center",
    )


# ─── Main index page ──────────────────────────────────────────────
def index() -> rx.Component:
    return rx.box(
        rx.vstack(
            # ── Header / Nav bar ──
            _glass_card(
                rx.hstack(
                    _page_heading(),
                    rx.spacer(),
                    rx.hstack(
                        rx.badge(
                            "AI Powered",
                            color_scheme="red",
                            variant="solid",
                            font_size="0.75em",
                            padding="0.4em 0.8em",
                            border_radius="8px",
                        ),
                        rx.badge(
                            "Socratic Method",
                            color_scheme="red",
                            variant="surface",
                            font_size="0.75em",
                            padding="0.4em 0.8em",
                            border_radius="8px",
                        ),
                        spacing="2",
                    ),
                    width="100%",
                    align="center",
                    padding_x="0",
                ),
                width="100%",
                text_align="center",
                padding="1em",
            ),

            # ── Divider ──
            rx.box(
                width="80px",
                height="3px",
                background=ACCENT,
                border_radius="2px",
                box_shadow=f"0 0 12px rgba(230, 57, 70, 0.4)",
            ),

            # ── Two-column layout ──
            rx.flex(
                # Left column: upload + results
                rx.vstack(
                    upload_box(),
                    rx.vstack(
                        rx.foreach(
                            rx.selected_files(UPLOAD_ID),
                            lambda file_name: rx.text(
                                file_name,
                                color=TEXT_MUTED,
                                font_size="0.85em",
                            ),
                        ),
                        width="100%",
                        align="start",
                    ),
                    rx.hstack(
                        rx.button(
                            rx.hstack(
                                rx.icon("scan-line", size=18),
                                rx.text("Analyze Image", font_weight="700"),
                                spacing="2",
                                align="center",
                            ),
                            on_click=TutorState.analyze_image(rx.upload_files(UPLOAD_ID)),
                            loading=TutorState.is_loading,
                            size="3",
                            flex="1",
                            background=ACCENT,
                            color="white",
                            border="none",
                            border_radius="12px",
                            cursor="pointer",
                            _hover={"background": ACCENT_HOVER, "transform": "translateY(-1px)"},
                            transition="all 0.2s ease",
                            box_shadow=f"0 4px 18px rgba(230, 57, 70, 0.35)",
                        ),
                        rx.button(
                            rx.hstack(
                                rx.icon("trash-2", size=16),
                                rx.text("Clear", font_weight="600"),
                                spacing="2",
                                align="center",
                            ),
                            on_click=TutorState.clear_image,
                            variant="outline",
                            size="3",
                            border="1px solid rgba(255, 255, 255, 0.3)",
                            color="#FFFFFF",
                            border_radius="12px",
                            background="rgba(255, 255, 255, 0.05)",
                            cursor="pointer",
                            _hover={"border_color": ACCENT, "color": ACCENT, "background": "rgba(230, 57, 70, 0.1)"},
                            transition="all 0.2s ease",
                        ),
                        width="100%",
                        spacing="3",
                    ),
                    # Progress indicator
                    rx.cond(
                        TutorState.is_loading,
                        rx.vstack(
                            rx.hstack(
                                rx.spinner(size="3", color=ACCENT),
                                rx.text(
                                    TutorState.analysis_progress,
                                    color=ACCENT,
                                    font_weight="800",
                                    font_size="1.2em",
                                ),
                                rx.text(
                                    "%",
                                    color=ACCENT,
                                    font_weight="800",
                                    font_size="1.2em",
                                ),
                                rx.text("—", color=TEXT_MUTED, font_size="1em"),
                                rx.text(
                                    TutorState.analysis_stage,
                                    color=TEXT_SECONDARY,
                                    font_size="0.92em",
                                    font_weight="500",
                                ),
                                spacing="2",
                                align="center",
                                width="100%",
                            ),
                            rx.progress(
                                value=TutorState.analysis_progress,
                                width="100%",
                                height="8px",
                                border_radius="4px",
                            ),
                            spacing="3",
                            align="center",
                            width="100%",
                            padding="1em",
                            background=CARD_BG,
                            border_radius="12px",
                            border=f"1px solid rgba(230, 57, 70, 0.3)",
                        ),
                    ),
                    error_text(),
                    response_box(),
                    extracted_text_box(),
                    math_analysis_box(),
                    spacing="4",
                    align="start",
                    width="100%",
                    flex="1",
                    min_width="0",
                ),
                # Right column: chat
                rx.box(chat_box(), width="100%", flex="1", min_width="0"),
                direction="row",
                align="stretch",
                width="100%",
                gap="1.5em",
                wrap="nowrap",
            ),

            # ── Footer ──
            rx.hstack(
                rx.text(
                    "© Socratic AI Tutor",
                    color=TEXT_MUTED,
                    font_size="0.8em",
                ),
                rx.text("·", color=TEXT_MUTED, font_size="0.8em"),
                rx.text(
                    "Powered by Groq & Pix2TeX",
                    color=TEXT_MUTED,
                    font_size="0.8em",
                ),
                spacing="2",
                justify="center",
                padding_top="1em",
            ),

            spacing="5",
            align="center",
            width="100%",
            max_width="1200px",
            margin="0 auto",
            padding="1.5em",
        ),
        # Credits box — fixed bottom-right
        rx.link(
            rx.hstack(
                rx.text("Made by", color=TEXT_MUTED, font_size="0.75em"),
                rx.text("Ayush Saini", color=TEXT_PRIMARY, font_size="0.75em", font_weight="700"),
                rx.icon("linkedin", size=13, color="#0A66C2"),
                spacing="1",
                align="center",
                background="rgba(15, 15, 18, 0.85)",
                padding="0.4em 0.8em",
                border_radius="8px",
                border=f"1px solid {CARD_BORDER}",
                backdrop_filter="blur(12px)",
            ),
            href="https://www.linkedin.com/in/ayush-saini-30a4a0372/",
            is_external=True,
            position="fixed",
            bottom="1em",
            right="1.5em",
            z_index="999",
            text_decoration="none",
        ),
        # Background image with cover
        min_height="100vh",
        width="100%",
        background=f"url('{BG_IMAGE}') center / cover no-repeat fixed",
        position="relative",
    )
