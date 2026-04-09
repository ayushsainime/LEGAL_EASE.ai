from pydantic import BaseModel


class AnalyzeImageResponse(BaseModel):
    filename: str
    image_url: str
    extracted_text: str
    problem_type: str
    structure_summary: str
    verification_summary: str
    normalized_expression: str
    tutor_response: str
