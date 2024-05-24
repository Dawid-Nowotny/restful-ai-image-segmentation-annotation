from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from user.service import UserServices
from models import User
from get_db import get_db
from .service import *

router = APIRouter()

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