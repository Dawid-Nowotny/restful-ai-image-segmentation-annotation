from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from validate_email import validate_email as validate_email_format

from models import User

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
        try:
            user = User(username=username, email=email, role="User")
            user.set_password(password)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))