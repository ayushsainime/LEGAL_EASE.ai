from __future__ import annotations

import tempfile
from pathlib import Path
from urllib.parse import urlparse

import httpx
from pydantic import BaseModel

import reflex as rx

from backend.services.document_service import extract_text, get_document_metadata
from backend.services.legal_service import simplify_document, chat_with_document
from backend.services.upload_service import save_upload_file
from tutor_app.constants import DEFAULT_MESSAGE, UPLOAD_ID


class ChatMessage(BaseModel):
    """A single chat message."""

    role: str  # "user" or "assistant"
    content: str


class LegalDocState(rx.State):
    """Reflex state that coordinates document upload, simplification, and chat."""

    # Document state
    uploaded_file_name: str = ""
    extracted_text: str = ""
    simplified_text: str = DEFAULT_MESSAGE
    document_summary: str = ""

    # Document metadata
    doc_file_name: str = ""
    doc_file_type: str = ""
    doc_page_count: int = 0
    doc_word_count: int = 0

    # UI state
    error_message: str = ""
    is_loading: bool = False
    show_raw_text: bool = False

    # Processing progress
    analysis_progress: int = 0
    analysis_stage: str = ""

    # Chat state
    chat_messages: list[ChatMessage] = []
    chat_input: str = ""
    is_chat_loading: bool = False

    async def process_document(self, files: list[rx.UploadFile]):
        """Upload a document, extract text, simplify, and generate summary."""
        self.is_loading = True
        self.error_message = ""
        self.extracted_text = ""
        self.uploaded_file_name = ""
        self.simplified_text = DEFAULT_MESSAGE
        self.document_summary = ""
        self.doc_file_name = ""
        self.doc_file_type = ""
        self.doc_page_count = 0
        self.doc_word_count = 0
        self.chat_messages = []
        self.show_raw_text = False
        self.analysis_progress = 0
        self.analysis_stage = "Preparing..."
        yield

        try:
            if not files:
                raise RuntimeError("Please upload a document before processing.")

            # Stage 1: Upload
            self.analysis_stage = "Uploading document..."
            self.analysis_progress = 10
            yield

            saved_path = await save_upload_file(files[0])
            self.uploaded_file_name = saved_path.name
            self.analysis_progress = 20
            self.analysis_stage = "Extracting text..."
            yield

            # Stage 2: Text extraction
            self.extracted_text = extract_text(saved_path)
            self.analysis_progress = 40
            self.analysis_stage = "Reading document metadata..."
            yield

            # Stage 3: Metadata
            metadata = get_document_metadata(saved_path, self.extracted_text)
            self.doc_file_name = metadata["file_name"]
            self.doc_file_type = metadata["file_type"]
            self.doc_page_count = metadata["page_count"]
            self.doc_word_count = metadata["word_count"]
            self.analysis_progress = 50
            self.analysis_stage = "Simplifying legal text..."
            yield

            # Stage 4: Simplify
            self.simplified_text = simplify_document(self.extracted_text)
            self.analysis_progress = 85
            self.analysis_stage = "Complete!"
            yield

            self.analysis_progress = 100
            yield

            # Seed the chat with a welcome message
            self.chat_messages = [
                ChatMessage(
                    role="assistant",
                    content=(
                        f"I've analyzed your document ({self.doc_file_name}). "
                        "You can ask me anything about it — clauses, terms, obligations, "
                        "or anything else you'd like clarified."
                    ),
                ),
            ]

        except Exception as error:
            self.error_message = str(error)
            self.simplified_text = (
                "I couldn't process that document. "
                "Please make sure it's a valid PDF, DOCX, or TXT file."
            )
        finally:
            self.is_loading = False
            self.analysis_progress = 0
            self.analysis_stage = ""

    async def send_chat_message(self) -> None:
        """Send a question about the document and get an AI response."""
        if not self.chat_input.strip():
            return
        if not self.extracted_text:
            return

        self.is_chat_loading = True
        user_message = self.chat_input.strip()
        self.chat_input = ""

        self.chat_messages.append(ChatMessage(role="user", content=user_message))

        try:
            response = chat_with_document(
                extracted_text=self.extracted_text,
                chat_history=[msg.dict() for msg in self.chat_messages],
                user_question=user_message,
            )
            self.chat_messages.append(ChatMessage(role="assistant", content=response))
        except Exception as error:
            self.chat_messages.append(
                ChatMessage(
                    role="assistant",
                    content=f"Sorry, something went wrong: {error}",
                )
            )
        finally:
            self.is_chat_loading = False

    def toggle_raw_text(self):
        """Toggle visibility of the raw extracted text."""
        self.show_raw_text = not self.show_raw_text

    def clear_document(self):
        """Clear the uploaded document and reset all state."""
        self.uploaded_file_name = ""
        self.extracted_text = ""
        self.simplified_text = DEFAULT_MESSAGE
        self.document_summary = ""
        self.doc_file_name = ""
        self.doc_file_type = ""
        self.doc_page_count = 0
        self.doc_word_count = 0
        self.error_message = ""
        self.chat_messages = []
        self.chat_input = ""
        self.is_chat_loading = False
        self.is_loading = False
        self.show_raw_text = False
        self.analysis_progress = 0
        self.analysis_stage = ""
        return rx.clear_selected_files(UPLOAD_ID)

    async def load_sample_document(self, url: str, display_name: str):
        """Download a sample PDF from a URL and process it."""
        self.is_loading = True
        self.error_message = ""
        self.extracted_text = ""
        self.uploaded_file_name = ""
        self.simplified_text = DEFAULT_MESSAGE
        self.document_summary = ""
        self.doc_file_name = ""
        self.doc_file_type = ""
        self.doc_page_count = 0
        self.doc_word_count = 0
        self.chat_messages = []
        self.show_raw_text = False
        self.analysis_progress = 0
        self.analysis_stage = "Downloading sample..."
        yield

        try:
            # Stage 1: Download
            self.analysis_progress = 10
            self.analysis_stage = "Downloading sample document..."
            yield

            async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
                response = await client.get(url)
                response.raise_for_status()

            # Save to a temp file
            suffix = Path(urlparse(url).path).suffix or ".pdf"
            tmp_path = Path(tempfile.gettempdir()) / f"legal_sample_{display_name.replace(' ', '_')}{suffix}"
            tmp_path.write_bytes(response.content)

            self.uploaded_file_name = display_name
            self.analysis_progress = 30
            self.analysis_stage = "Extracting text..."
            yield

            # Stage 2: Text extraction
            self.extracted_text = extract_text(tmp_path)
            self.analysis_progress = 50
            self.analysis_stage = "Reading document metadata..."
            yield

            # Stage 3: Metadata
            metadata = get_document_metadata(tmp_path, self.extracted_text)
            self.doc_file_name = display_name
            self.doc_file_type = metadata["file_type"]
            self.doc_page_count = metadata["page_count"]
            self.doc_word_count = metadata["word_count"]
            self.analysis_progress = 60
            self.analysis_stage = "Simplifying legal text..."
            yield

            # Stage 4: Simplify
            self.simplified_text = simplify_document(self.extracted_text)
            self.analysis_progress = 100
            self.analysis_stage = "Complete!"
            yield

            # Seed the chat with a welcome message
            self.chat_messages = [
                ChatMessage(
                    role="assistant",
                    content=(
                        f"I've analyzed the sample document ({display_name}). "
                        "You can ask me anything about it — clauses, terms, obligations, "
                        "or anything else you'd like clarified."
                    ),
                ),
            ]

            # Clean up temp file
            try:
                tmp_path.unlink()
            except Exception:
                pass

        except Exception as error:
            self.error_message = str(error)
            self.simplified_text = (
                "I couldn't process that sample document. Please try again."
            )
        finally:
            self.is_loading = False
            self.analysis_progress = 0
            self.analysis_stage = ""

    def set_chat_input(self, value: str):
        """Explicit setter for chat input."""
        self.chat_input = value
