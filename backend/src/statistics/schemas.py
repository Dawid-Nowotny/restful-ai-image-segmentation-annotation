from pydantic import BaseModel

class TopTagResponse(BaseModel):
    tag: str
    count: int

class TopClassResponse(BaseModel):
    class_name: str
    count: int

class TopUploaderResponse(BaseModel):
    username: str
    upload_count: int

class TopCommenterResponse(BaseModel):
    username: str
    comment_count: int

class ModeratedImagesResponse(BaseModel):
    username: str
    moderated_count: int