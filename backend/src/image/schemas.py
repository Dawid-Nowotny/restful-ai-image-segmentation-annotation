from pydantic import BaseModel
from fastapi import Form

from dataclasses import dataclass
from typing import Optional, List

@dataclass
class ImageData:
    uploader_id: int = Form()
    moderator_id: Optional[int] = Form(None)
    threshold: float = Form(ge=0.0, le=1.0)

class TagRequest(BaseModel):
    tag: str

class CommentRequest(BaseModel):
    super_tag: bool
    tags: List[TagRequest]