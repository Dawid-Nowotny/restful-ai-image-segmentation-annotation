from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session
from typing import List

from .schemas import ModeratorResponse, UserResponse, SuperTagIdRequest

from models import User
from get_db import get_db
from .service import AdminServices, ModeratorServices

from user.service import UserServices
from image.service import ImageServices, CommentServices
from image.schemas import CommentRequest

router = APIRouter()

@router.get("/moderators-list", response_model=List[ModeratorResponse])
def get_moderators(db: Session = Depends(get_db)):
    admin_service = AdminServices()
    moderators = admin_service.get_moderators(db)

    return moderators

@router.get("/users-list", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    admin_service = AdminServices()
    users = admin_service.get_users(db)

    return users

@router.put("/make-moderator/{username}")
async def make_moderator(
    username: str,
    current_user: User = Depends(UserServices.get_current_user),
    db: Session = Depends(get_db)
    ):
    admin_service = AdminServices()

    admin_service.check_if_admin(current_user)
    await admin_service.make_moderator(username, db)

    return {"message": "Rola moderatora została pomyślnie nadana"}

@router.put("/assign-moderator/{image_id}/{username}")
async def assign_moderator_to_image(
    username: str,
    image_id: int = Path(..., ge=0),
    current_user: User = Depends(UserServices.get_current_user),
    db: Session = Depends(get_db)
    ):
    admin_service = AdminServices()

    admin_service.check_if_admin(current_user)
    await admin_service.assign_moderator_to_image(image_id, username, db)

    return {"message": "Moderator został nadany do obrazka"}

@router.post("/add-super-tag", status_code=status.HTTP_201_CREATED)
async def create_comment_super_tag(
    request: SuperTagIdRequest,
    comment_data: CommentRequest,
    current_user: User = Depends(UserServices.get_current_user),
    db: Session = Depends(get_db)
    ):
    moderator_service = ModeratorServices()
    image_service = ImageServices()
    comment_service = CommentServices()
    
    image = image_service.get_single_image(request.image_id, db)
    comment_service.check_if_image_has_supertags(image, db)
    moderator_service.check_if_admin_or_moderator(current_user)
    moderator_service.check_if_moderator_is_assigned_to_image(image, current_user)

    tags = [await comment_service.create_tag(tag_data.tag, db) for tag_data in comment_data.tags]

    await comment_service.create_comment(request.image_id, current_user, comment_data, tags, db)

    return {"message": "Super tag został dodany do obrazka"}