from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .service import UserService
from .schemas import UserCreateSchema, LoginInfo

from get_db import get_db

router = APIRouter()

@router.post("/login", status_code=status.HTTP_200_OK)
def login(login_info: LoginInfo, db: Session = Depends(get_db)):
    service = UserService(db)

    user = service.authenticate_user(login_info.Username, login_info.Password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"access_token": user.username}

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreateSchema, db: Session = Depends(get_db)):
    service = UserService(db)

    if service.check_if_user_exists(user.Username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = service.create_user(user.Username, user.Email, user.Password)

    return {
        "username": new_user.username,
        "email": new_user.email,
    }