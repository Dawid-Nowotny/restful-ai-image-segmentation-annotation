from fastapi import Form

from dataclasses import dataclass

@dataclass
class ImageData:
    uploader_id: int = Form()
    moderator_id: int = Form()