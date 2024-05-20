from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from .service import *
from .schemas import UserCreateSchema, UserOut
from get_db import get_db

router = APIRouter()

@router.post("/login")
def login(login_info: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
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

@router.get("/me")
async def read_users_me(
    current_user: Annotated[User, Depends(UserServices.get_current_active_user)], 
):  
    if current_user.secret_key is not None:
        return UserOut(id=current_user.id, username=current_user.username, email=current_user.email, role=current_user.role, totp_enabled=True)
    else:
        return UserOut(id=current_user.id, username=current_user.username, email=current_user.email, role=current_user.role, totp_enabled=False)

@router.post("/generate-qr", status_code=status.HTTP_201_CREATED)
async def generate_qr(
    current_user: Annotated[User, Depends(UserServices.get_current_active_user)], db: Session = Depends(get_db)
    ):
    totp_service = TOTPServices()

    if current_user.secret_key is not None:
        return {"message": "Konto posiada już weryfikację dwuetapową"}

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
