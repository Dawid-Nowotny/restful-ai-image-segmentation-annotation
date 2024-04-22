from dataclasses import dataclass
from fastapi import Form

@dataclass
class ImageData:
  uploader_id: int = Form()
  moderator_id: int = Form()