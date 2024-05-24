from pydantic import BaseModel

class ModeratorResponse(BaseModel):
    username: str

    class Config:
        orm_mode = True