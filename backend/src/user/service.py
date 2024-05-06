from sqlalchemy.orm import Session

from models import User

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def check_if_user_exists(self, username: str):
        user = self.db.query(User).filter(User.username == username).first()
        if user:
            return user
        return False

    def authenticate_user(self, username: str, password: str):
        user = self.db.query(User).filter(User.username == username).first()

        if user and user.verify_password(password):
            return user
        return False

    def create_user(self, Username: str, Email: str, Password: str):
        new_User = User(username=Username, email=Email, role="NEW_USER")
        new_User.set_password(Password)
        self.db.add(new_User)
        self.db.commit()
        self.db.refresh(new_User)
        return new_User