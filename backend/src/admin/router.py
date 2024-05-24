from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .schemas import ModeratorResponse
from user.service import UserServices
from models import User
from get_db import get_db
from .service import *

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