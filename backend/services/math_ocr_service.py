from __future__ import annotations

from pathlib import Path

from PIL import Image
from pix2tex.cli import LatexOCR

_latex_ocr_model: LatexOCR | None = None


def get_latex_ocr_model() -> LatexOCR:
    """Create the pix2tex model once and reuse it."""
    global _latex_ocr_model

    if _latex_ocr_model is None:
        _latex_ocr_model = LatexOCR()

    return _latex_ocr_model


def extract_latex_from_image(image_path: Path) -> str:
    """Run pix2tex on a saved image and return LaTeX."""
    try:
        model = get_latex_ocr_model()
        with Image.open(image_path) as image:
            latex = model(image).strip()

        if not latex:
            raise RuntimeError("No math expression was detected in the image.")

        return latex
    except Exception as error:
        raise RuntimeError(f"Math OCR failed: {error}") from error
