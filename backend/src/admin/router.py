from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from .schemas import ModeratorResponse
from models import User
from get_db import get_db
from .service import *

from user.service import UserServices
from image.service import ImageServices, CommentServices
from image.schemas import CommentRequest

router = APIRouter()

@router.get("/moderators-list", response_model=List[ModeratorResponse])
def get_moderators(db: Session = Depends(get_db)):
    admin_service = AdminServices()
    moderators = admin_service.get_moderators(db)

    return moderators

@router.put("/make_moderator/{username}")
def make_moderator(
    username: str,
    current_user: User = Depends(UserServices.get_current_user),
    db: Session = Depends(get_db)
    ):
    admin_service = AdminServices()

    admin_service.check_if_admin(current_user)
    admin_service.make_moderator(username, db)

    return {"message": "Rola moderatora została pomyślnie nadana"}

@router.put("/assign-moderator/{image_id}/{username}")
def assign_moderator_to_image(
    image_id: int,
    username: str,
    current_user: User = Depends(UserServices.get_current_user),
    db: Session = Depends(get_db)
    ):
    admin_service = AdminServices()

    admin_service.check_if_admin(current_user)
    admin_service.assign_moderator_to_image(image_id, username, db)

    return {"message": "Moderator został nadany do obrazka"}

@router.post("/add-super-tag", status_code=status.HTTP_201_CREATED)
def create_comment_super_tag(
    image_id: int,
    comment_data: CommentRequest,
    current_user: User = Depends(UserServices.get_current_user),
    db: Session = Depends(get_db)
    ):
    moderator_service = ModeratorServices()
    image_service = ImageServices()
    comment_services = CommentServices()

    moderator_service.check_if_admin_or_moderator(current_user)
    image = image_service.get_single_image(image_id, db)
    moderator_service.check_if_moderator_is_assigned_to_image(image, current_user)

    tags = [comment_services.create_tag(tag_data.tag, db) for tag_data in comment_data.tags]

    comment_services.create_comment(image_id, current_user, comment_data, tags, db)

    return {"message": "Super tag został dodany do obrazka"}