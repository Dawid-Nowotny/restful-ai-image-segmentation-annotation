from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from validate_email import validate_email as validate_email_format
from jose import JWTError, jwt

from datetime import datetime, timedelta, timezone
from typing import Annotated

from .jwt_config import SECRET_KEY, ALGORITHM
from .schemas import TokenData, UserOut
from get_db import get_db
try:
    from models import User
except:
    from src.models import User

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

    def create_user(self, username: str, email: str, password: str, db: Session) -> User:
        user = User(username=username, email=email, role="User")
        user.set_password(password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
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
    def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserOut:
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
        
        user_out = UserOut(username=user.username, email=user.email, role=user.role)
        return user_out
    
    @staticmethod
    async def get_current_active_user(current_user: Annotated[UserOut, Depends(get_current_user)]) -> UserOut:
        return current_user