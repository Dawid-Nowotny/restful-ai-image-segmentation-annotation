from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from .service import *
from .schemas import UserCreateSchema, UserOut
from get_db import get_db

router = APIRouter()

@router.post("/login")
def login(
    login_info: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
    ):
    user_service = UserServices()
    totp_en = False

    user = user_service.authenticate_user(login_info.username, login_info.password, db)
    access_token = user_service.create_access_token(data={"sub": user.username})

    if user.secret_key is not None:
        totp_en = True

    return {"access_token": access_token, "token_type": "bearer", "totp_enabled": totp_en}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreateSchema, db: Session = Depends(get_db)):
    user_service = UserServices()

    user_service.check_if_user_exists(user.username, user.email, db)

    user = await user_service.create_user(user.username, user.email, user.password, db)
    access_token = user_service.create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def read_users_me(
    current_user: Annotated[User, Depends(UserServices.get_current_active_user)]
    ):  
    totp_enabled = current_user.secret_key is not None
    user_data = current_user.__dict__
    user_data['totp_enabled'] = totp_enabled
    return user_data

@router.get("/get-profile-info/{username}")
def profile_info(username: str, db: Session = Depends(get_db)):
    user_service = UserServices()
    user = user_service.get_user_by_username(username, db)
    images_count = user_service.count_user_images(user, db)

    return {
        "username": user.username, 
        "role": user.role, 
        "images_count": images_count
    }

@router.post("/generate-qr", status_code=status.HTTP_201_CREATED)
async def generate_qr(
    current_user: Annotated[User, Depends(UserServices.get_current_active_user)], 
    db: Session = Depends(get_db)
    ):
    totp_service = TOTPServices()

    secret_key = await totp_service.generate_secret_key()
    await totp_service.set_secret_key(current_user, secret_key, db)
    qr_code = totp_service.generate_qr_code(current_user.username, secret_key)

    return Response(
        content=qr_code, 
        media_type="image/png"
        )

@router.post("/verify-code")
async def verify_2fa(
    token: str, current_user: User = Depends(UserServices.get_current_user)
    ):
    totp_service = TOTPServices()
    await totp_service.verify_2fa_token(token, current_user)

    return {"message": "Kod 2FA został pomyślnie zweryfikowany"}