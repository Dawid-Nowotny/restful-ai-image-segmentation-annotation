from dataclasses import dataclass
from pydantic import BaseModel
from fastapi import Form

# !!można użyć pydantica, ale wtedy parametry będą jako query
# class ImageData(BaseModel):
#   uploader_id: int
#   moderator_id: int

@dataclass
class ImageData:
  uploader_id: int = Form()
  moderator_id: int = Form()