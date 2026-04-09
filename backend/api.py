from __future__ import annotations

from fastapi import FastAPI, File, UploadFile
import reflex as rx

from backend.models import AnalyzeImageResponse
from backend.services.math_ocr_service import extract_latex_from_image
from backend.services.math_service import analyze_math_expression
from backend.services.tutor_service import ask_socratic_question
from backend.services.upload_service import save_upload_file

fastapi_app = FastAPI(title="Socratic AI Tutor API")


@fastapi_app.get("/api/health")
async def health_check() -> dict[str, str]:
    """Small health route to confirm the backend is running."""
    return {"status": "ok"}


@fastapi_app.post("/api/analyze-image", response_model=AnalyzeImageResponse)
async def analyze_image_api(file: UploadFile = File(...)) -> AnalyzeImageResponse:
    """Analyze an uploaded image through a plain FastAPI endpoint."""
    saved_path = await save_upload_file(file)
    extracted_text = extract_latex_from_image(saved_path)
    math_analysis = analyze_math_expression(extracted_text)
    tutor_response = ask_socratic_question(
        extracted_text=extracted_text,
        problem_type=math_analysis.problem_type,
        structure_summary=math_analysis.structure_summary,
        verification_summary=math_analysis.verification_summary,
    )

    return AnalyzeImageResponse(
        filename=saved_path.name,
        image_url=rx.get_upload_url(saved_path.name),
        extracted_text=extracted_text,
        problem_type=math_analysis.problem_type,
        structure_summary=math_analysis.structure_summary,
        verification_summary=math_analysis.verification_summary,
        normalized_expression=math_analysis.normalized_expression,
        tutor_response=tutor_response,
    )
