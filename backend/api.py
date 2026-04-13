from __future__ import annotations

from fastapi import FastAPI, File, UploadFile

from backend.models import ProcessDocumentResponse
from backend.services.document_service import extract_text, get_document_metadata
from backend.services.legal_service import simplify_document
from backend.services.upload_service import save_upload_file

fastapi_app = FastAPI(title="Legal Doc AI API")


@fastapi_app.get("/api/health")
async def health_check() -> dict[str, str]:
    """Small health route to confirm the backend is running."""
    return {"status": "ok"}


@fastapi_app.post("/api/process-document", response_model=ProcessDocumentResponse)
async def process_document_api(file: UploadFile = File(...)) -> ProcessDocumentResponse:
    """Process an uploaded document through a plain FastAPI endpoint."""
    saved_path = await save_upload_file(file)
    extracted = extract_text(saved_path)
    metadata = get_document_metadata(saved_path, extracted)
    simplified = simplify_document(extracted)

    return ProcessDocumentResponse(
        filename=metadata["file_name"],
        file_type=metadata["file_type"],
        page_count=metadata["page_count"],
        word_count=metadata["word_count"],
        extracted_text=extracted,
        simplified_text=simplified,
    )