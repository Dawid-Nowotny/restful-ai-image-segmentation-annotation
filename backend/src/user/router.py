from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

import json

from .service import *
from .schemas import UserCreateSchema, LoginInfo
from get_db import get_db

router = APIRouter()

@router.post("/login")
def login(login_info: LoginInfo, db: Session = Depends(get_db)):
    user_service = UserServices()

    user = user_service.authenticate_user(login_info.username, login_info.password, db)
    
    return Response(
        content=json.dumps({"id": user.id, "username": user.username, "email": user.email}),
        media_type="application/json",
        status_code=status.HTTP_200_OK,
    )

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreateSchema, db: Session = Depends(get_db)):
    user_service = UserServices()

    user_service.check_if_user_exists(user.username, user.email, db)

    user = user_service.create_user(user.username, user.email, user.password, db)

    return Response(
        content=json.dumps({"id": user.id, "username": user.username, "email": user.email}),
        media_type="application/json",
        status_code=status.HTTP_201_CREATED,
    )