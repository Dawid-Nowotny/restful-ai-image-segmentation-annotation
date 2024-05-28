from pydantic import BaseModel

class TagResponse(BaseModel):
    tag: str
    count: int

class TopUploaderResponse(BaseModel):
    username: str
    upload_count: int

class TopCommenterResponse(BaseModel):
    username: str
    comment_count: int