from __future__ import annotations

from pathlib import Path
import shutil

from PIL import Image
from pix2tex.cli import LatexOCR
from munch import Munch
import pix2tex

_latex_ocr_model: LatexOCR | None = None

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOCAL_CHECKPOINT_DIR = PROJECT_ROOT / "models" / "pix2tex"
LOCAL_CHECKPOINT = LOCAL_CHECKPOINT_DIR / "weights.pth"
LOCAL_RESIZER = LOCAL_CHECKPOINT_DIR / "image_resizer.pth"


def _package_checkpoint_dir() -> Path:
    return Path(pix2tex.__file__).resolve().parent / "model" / "checkpoints"


def _copy_package_weights_to_local() -> None:
    """Copy already-downloaded package weights into project-local storage."""
    package_dir = _package_checkpoint_dir()
    LOCAL_CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    package_weights = package_dir / "weights.pth"
    package_resizer = package_dir / "image_resizer.pth"

    if package_weights.exists() and not LOCAL_CHECKPOINT.exists():
        shutil.copy2(package_weights, LOCAL_CHECKPOINT)
    if package_resizer.exists() and not LOCAL_RESIZER.exists():
        shutil.copy2(package_resizer, LOCAL_RESIZER)


def get_latex_ocr_model() -> LatexOCR:
    """Create the pix2tex model once and reuse it."""
    global _latex_ocr_model

    if _latex_ocr_model is None:
        _copy_package_weights_to_local()

        if LOCAL_CHECKPOINT.exists():
            _latex_ocr_model = LatexOCR(
                Munch(
                    {
                        "config": "settings/config.yaml",
                        "checkpoint": str(LOCAL_CHECKPOINT),
                        "no_cuda": True,
                        "no_resize": False,
                    }
                )
            )
        else:
            # First-ever run: pix2tex downloads into its package dir.
            _latex_ocr_model = LatexOCR()
            _copy_package_weights_to_local()

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
