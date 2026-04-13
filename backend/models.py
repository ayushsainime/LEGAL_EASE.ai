from pydantic import BaseModel


class ProcessDocumentResponse(BaseModel):
    filename: str
    file_type: str
    page_count: int
    word_count: int
    extracted_text: str
    simplified_text: str