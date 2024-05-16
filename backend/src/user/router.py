from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from .service import *
from .schemas import UserCreateSchema, UserOut
from get_db import get_db

router = APIRouter()

@router.post("/login")
async def login(login_info: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user_service = UserServices()
    user = user_service.authenticate_user(login_info.username, login_info.password, db)
    access_token = user_service.create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreateSchema, db: Session = Depends(get_db)):
    user_service = UserServices()

    user_service.check_if_user_exists(user.username, user.email, db)

    user = user_service.create_user(user.username, user.email, user.password, db)
    access_token = user_service.create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def read_users_me(
    current_user: Annotated[UserOut, Depends(UserServices.get_current_active_user)], 
):
    return current_user