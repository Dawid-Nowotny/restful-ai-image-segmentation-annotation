from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from typing import List

from get_db import get_db
from models import User
from .service import ImageStatsServices, UserStatsServices
from .schemas import TopTagResponse, MonthlyTagResponse, TopClassResponse, MonthlyClassResponse, TopUploaderResponse, TopCommenterResponse, ModeratedImagesResponse
from user.service import UserServices
from admin.service import ModeratorServices

router = APIRouter()

@router.get("/top-tags/{limit}", response_model=List[TopTagResponse])
def get_top_tags(limit: int = Path(..., gt=0), db: Session = Depends(get_db)):
    image_stats_service = ImageStatsServices()
    tags = image_stats_service.get_top_tags(limit, db)
    return tags

@router.get("/popular-tags-by-month", response_model=List[MonthlyTagResponse])
def get_popular_tags_by_month(db: Session = Depends(get_db)):
    image_stats_service = ImageStatsServices()
    popular_tags = image_stats_service.get_popular_tags_by_month(db)
    return popular_tags

@router.get("/top-classes/{limit}", response_model=List[TopClassResponse])
def get_top_classes(limit: int = Path(..., gt=0), db: Session = Depends(get_db)):
    image_stats_service = ImageStatsServices()
    top_classes = image_stats_service.get_top_classes(limit, db)
    return top_classes

@router.get("/popular-classes-by-month", response_model=List[MonthlyClassResponse])
def get_popular_classes_by_month(db: Session = Depends(get_db)):
    image_stats_service = ImageStatsServices()
    popular_classes = image_stats_service.get_popular_classes_by_month(db)
    return popular_classes

@router.get("/top-uploaders/{limit}", response_model=List[TopUploaderResponse])
def get_top_uploaders(
    limit: int = Path(..., gt=0), 
    current_user: User = Depends(UserServices.get_current_user),
    db: Session = Depends(get_db)
    ):
    moderator_service = ModeratorServices()
    user_stats_service = UserStatsServices()

    moderator_service.check_if_admin_or_moderator(current_user)
    top_uploaders = user_stats_service.get_top_uploaders(limit, db)
    return top_uploaders

@router.get("/top-commenters/{limit}", response_model=List[TopCommenterResponse])
def get_top_commenters(
    limit: int = Path(..., gt=0), 
    current_user: User = Depends(UserServices.get_current_user),
    db: Session = Depends(get_db)
    ):
    moderator_service = ModeratorServices()    
    user_stats_service = UserStatsServices()
    
    moderator_service.check_if_admin_or_moderator(current_user)
    top_commenters = user_stats_service.get_top_commenters(limit, db)
    return top_commenters

@router.get("/moderated-images/{limit}", response_model=List[ModeratedImagesResponse])
def get_moderated_images_count(
    limit: int = Path(..., gt=0), 
    current_user: User = Depends(UserServices.get_current_user),
    db: Session = Depends(get_db)
    ):
    moderator_service = ModeratorServices()
    user_stats_service = UserStatsServices()

    moderator_service.check_if_admin_or_moderator(current_user)
    moderated_counts = user_stats_service.get_moderated_images_count(limit, db)
    return moderated_counts