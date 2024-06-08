from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

from .service import UserServices, TOTPServices
from .schemas import UserCreateSchema, UserUpdateSchema, UserOut, VerifyTotpRequest, DisableTOTPRequest
from models import User
from get_db import get_db

router = APIRouter()

@router.post("/login")
def login(
    response: Response,
    login_info: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
    ):
    user_service = UserServices()
    totp_en = False

    user = user_service.authenticate_user(login_info.username, login_info.password, db)
    access_token = user_service.create_access_token(data={"sub": user.username})

    if user.secret_key is not None:
        totp_en = True

    response.set_cookie(key="access_token",value=f"Bearer {access_token}", httponly=True, samesite="none", secure=True);  
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "totp_enabled": totp_en
    }

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreateSchema, db: Session = Depends(get_db)):
    user_service = UserServices()

    user_service.check_if_user_exists(user.username, user.email, db)

    user = await user_service.create_user(user.username, user.email, user.password, db)
    access_token = user_service.create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@router.patch("/update-user")
async def update_user(
    current_user: Annotated[User, Depends(UserServices.get_current_active_user)],
    user_data_update: UserUpdateSchema,
    db: Session= Depends(get_db),
    ):
    user_service = UserServices()
    
    user_service.check_password(current_user, user_data_update.old_password)
    user_service.check_username_email_availability_for_current_user(user_data_update, current_user, db)
    user = await user_service.update_user(current_user, user_data_update, db)
    access_token = user_service.create_access_token(data={"sub": user.username})

    return {
        "username": user.username,
        "email": user.email,
        "access_token": access_token,
        "token_type": "bearer"
    }

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
    request: VerifyTotpRequest, current_user: User = Depends(UserServices.get_current_user)
    ):
    totp_service = TOTPServices()
    await totp_service.verify_2fa_token(request.token, current_user)

    return {"message": "Kod 2FA został pomyślnie zweryfikowany"}

@router.put("/disable-totp")
async def disable_2fa(
    request: DisableTOTPRequest,
    current_user: Annotated[User, Depends(UserServices.get_current_active_user)], 
    db: Session = Depends(get_db)
    ):
    user_service = UserServices()
    totp_service = TOTPServices()

    user_service.check_password(current_user, request.password)
    await totp_service.disable_totp(current_user, db)

    return {"message": "Dwuetapowa weryfikacja została wyłączona"}