from __future__ import annotations

import reflex as rx

from backend.services.math_ocr_service import extract_latex_from_image
from backend.services.math_service import analyze_math_expression
from backend.services.tutor_service import ask_socratic_question
from backend.services.upload_service import save_upload_file
from tutor_app.constants import DEFAULT_MESSAGE


class TutorState(rx.State):
    """Reflex state that coordinates the upload flow."""

    uploaded_image_url: str = ""
    extracted_text: str = ""
    problem_type: str = ""
    structure_summary: str = ""
    verification_summary: str = ""
    normalized_expression: str = ""
    tutor_response: str = DEFAULT_MESSAGE
    error_message: str = ""
    is_loading: bool = False

    async def analyze_image(self, files: list) -> None:
        """Save the image, extract text, and ask for one Socratic hint."""
        self.is_loading = True
        self.error_message = ""
        self.extracted_text = ""
        self.problem_type = ""
        self.structure_summary = ""
        self.verification_summary = ""
        self.normalized_expression = ""
        self.tutor_response = DEFAULT_MESSAGE

        try:
            if not files:
                raise RuntimeError("Please upload an image before analyzing it.")

            saved_path = await save_upload_file(files[0])
            self.uploaded_image_url = rx.get_upload_url(saved_path.name)
            self.extracted_text = extract_latex_from_image(saved_path)
            math_analysis = analyze_math_expression(self.extracted_text)
            self.problem_type = math_analysis.problem_type
            self.structure_summary = math_analysis.structure_summary
            self.verification_summary = math_analysis.verification_summary
            self.normalized_expression = math_analysis.normalized_expression
            self.tutor_response = ask_socratic_question(
                extracted_text=self.extracted_text,
                problem_type=self.problem_type,
                structure_summary=self.structure_summary,
                verification_summary=self.verification_summary,
            )
        except Exception as error:
            self.error_message = str(error)
            self.tutor_response = "I couldn't analyze that image yet. Try a clearer photo."
        finally:
            self.is_loading = False
