from fastapi import Form

from typing import Optional
from dataclasses import dataclass

@dataclass
class ImageData:
    uploader_id: int = Form()
    moderator_id: Optional[int] = Form(None)
    threshold: float = Form(ge=0.0, le=1.0)