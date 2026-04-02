from pathlib import Path
from uuid import uuid4

UPLOAD_DIR = Path("uploads")


def save_uploaded_file(file, prefix: str = "img") -> str | None:
    if file is None:
        return None
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    ext = Path(file.name).suffix or ".jpg"
    file_name = f"{prefix}_{uuid4().hex[:10]}{ext}"
    target = UPLOAD_DIR / file_name
    target.write_bytes(file.getbuffer())
    return str(target)
