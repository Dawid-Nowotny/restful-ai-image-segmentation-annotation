from fastapi import Form

from typing import Optional
from dataclasses import dataclass

@dataclass
class ImageData:
    uploader_id: int = Form()
    moderator_id: Optional[int] = Form(None)
    iou_threshold: float = Form(default=0.6, ge=0.0, le=1.0)