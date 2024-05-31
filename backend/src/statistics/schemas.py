from pydantic import BaseModel
from typing import List, Dict, Any

class TopTagResponse(BaseModel):
    tag: str
    count: int

class MonthlyTagResponse(BaseModel):
    year: int
    month: str
    top_tag: Dict[str, Any]

class TopClassResponse(BaseModel):
    class_name: str
    count: int

class MonthlyClassResponse(BaseModel):
    year: int
    month: str
    top_classes: Dict[str, Any]

class TopUploaderResponse(BaseModel):
    username: str
    upload_count: int

class TopCommenterResponse(BaseModel):
    username: str
    comment_count: int

class ModeratedImagesResponse(BaseModel):
    username: str
    moderated_count: int