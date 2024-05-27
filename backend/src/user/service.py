import pyotp
import pyqrcode
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import func
from validate_email import validate_email as validate_email_format
from jose import JWTError, jwt

import io

from datetime import datetime, timedelta, timezone
from typing import Annotated, Tuple

from .jwt_config import SECRET_KEY, ALGORITHM
from .schemas import TokenData

try:
    from models import User, Image
    from get_db import get_db
except:
    from src.models import User, Image
    from src.get_db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserServices:
    def check_if_user_exists(self, username: str, email: str, db: Session) -> None:
        username = db.query(User).filter(User.username == username).first()

        if username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nazwa użytkownika zajęta")

        user_email = db.query(User).filter(User.email == email).first()

        if user_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail zajęty")

    def authenticate_user(self, username: str, password: str, db: Session) -> User:
        is_email = validate_email_format(username)
        
        if is_email:
            user = db.query(User).filter(User.email == username).first()
        else: 
            user = db.query(User).filter(User.username == username).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Niewłaściwa nazwa użytkownika")

        if user and user.verify_password(password):
            return user
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Niepoprawne hasło")

    async def create_user(self, username: str, email: str, password: str, db: Session) -> User:
        user = User(username=username, email=email, role="User")
        user.set_password(password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_user_by_username(self, username: str, db: Session) -> User:
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono użytkownika")
        return user
    
    def count_user_images(self, user: User, db: Session) -> int:
        images_count = db.query(func.count(Image.id)).filter(Image.uploader_id == user.id).scalar()
        return images_count
    
    @staticmethod
    def __get_user_by_username(username, db: Session) -> User: 
        user = db.query(User).filter(User.username == username).first()
        return user
    
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        
        user = UserServices.__get_user_by_username(token_data.username, db)
        
        if user is None:
            raise credentials_exception
        
        return user
    
    @staticmethod
    async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
        return current_user
    
class TOTPServices:
    async def generate_secret_key(self) -> str:
        return pyotp.random_base32()

    def generate_qr_code(self, username: str, secret_key: str) -> bytes:
        uri = pyotp.totp.TOTP(secret_key).provisioning_uri(username, issuer_name="RAISA")
        qr_code = pyqrcode.create(uri)
        buffer = io.BytesIO()
        qr_code.png(buffer, scale=5)
        return buffer.getvalue()
        
    async def set_secret_key(self, user: User, secret_key: str, db: Session) -> None:
        user.secret_key = secret_key
        db.add(user)
        db.commit()
        db.refresh(user)

    async def verify_2fa_token(self, token: str, user: User) -> None:
        totp = pyotp.TOTP(user.secret_key)
        valid = totp.verify(token)

        if not valid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nieprawidłowy kod 2FA")