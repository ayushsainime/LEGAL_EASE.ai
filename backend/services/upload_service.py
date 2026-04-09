from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import reflex as rx


async def save_upload_file(upload_file: Any) -> Path:
    """Save an uploaded file into Reflex's upload directory."""
    upload_dir = rx.get_upload_dir()
    upload_dir.mkdir(parents=True, exist_ok=True)

    original_name = Path(
        getattr(upload_file, "name", None)
        or getattr(upload_file, "filename", None)
        or "math_homework.png"
    ).name
    saved_name = f"{int(time.time())}_{original_name}"
    saved_path = upload_dir / saved_name

    file_bytes = await upload_file.read()
    saved_path.write_bytes(file_bytes)
    return saved_path
