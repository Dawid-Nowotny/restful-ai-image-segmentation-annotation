from pydantic import BaseModel, ConfigDict
from typing import List

class ModeratorResponse(BaseModel):
    username: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    username: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)

class SuperTagIdRequest(BaseModel):
    image_id: int