from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from typing import List

from .service import ImageStatsServices, UserStatsServices
from .schemas import TagResponse, TopUploaderResponse
from get_db import get_db

router = APIRouter()

@router.get("/top_tags/{limit}", response_model=List[TagResponse])
def get_top_tags(limit: int = Path(..., gt=0), db: Session = Depends(get_db)):
    image_stats_service = ImageStatsServices()
    tags = image_stats_service.get_top_tags(limit, db)
    return tags

@router.get("/top_uploaders/{limit}", response_model=List[TopUploaderResponse])
def get_top_uploaders(limit: int = Path(..., gt=0), db: Session = Depends(get_db)):
    user_stats_service = UserStatsServices()
    top_uploaders = user_stats_service.get_top_uploaders(limit, db)
    return top_uploaders