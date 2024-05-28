from pydantic import BaseModel
from typing import List

class ModeratorResponse(BaseModel):
    username: str

    class Config:
        from_attributes = True

class SuperTagIdRequest(BaseModel):
    image_id: int