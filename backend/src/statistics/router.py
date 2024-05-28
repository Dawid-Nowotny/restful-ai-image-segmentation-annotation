from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from typing import List

from .service import ImageStatsServices, UserStatsServices
from .schemas import TagResponse, TopUploaderResponse, TopCommenterResponse, ModeratedImagesResponse
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

@router.get("/top_commenters/{limit}", response_model=List[TopCommenterResponse])
def get_top_commenters(limit: int = Path(..., gt=0), db: Session = Depends(get_db)):
    user_stats_service = UserStatsServices()
    top_commenters = user_stats_service.get_top_commenters(limit, db)
    return top_commenters

@router.get("/moderated_images/{limit}", response_model=List[ModeratedImagesResponse])
def get_moderated_images_count(limit: int = Path(..., gt=0), db: Session = Depends(get_db)):
    user_stats_service = UserStatsServices()
    moderated_counts = user_stats_service.get_moderated_images_count(limit, db)
    return moderated_counts