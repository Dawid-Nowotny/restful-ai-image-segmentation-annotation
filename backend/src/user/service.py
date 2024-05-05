#services

#from .backend.src.models import User
from models import User
#from .schemas import UserCreateSchema, LoginInfo
from sqlalchemy.orm import Session


#async def authenticate_user(db, username: str, password: str):
#    user = await User.get_user(db, username)
#    if not user:
#        return False
#    if not user.verify_password(password):
#        return False
#    return user

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def check_if_user_exists(self, username: str):
        user = self.db.query(User).filter(User.username == username).first()
        if user:
            return user
        return False

    def authenticate_user(self, username: str, password: str):
        #print("testauth1")
        user = self.db.query(User).filter(User.username == username).first()
        #print("testauth2")
        #print("User:", user)
        #if user:
        #    print("IFUSER", user)
        #print("IS AUTH: ", user.verify_password(password))
        #print("testauth3")
        if user and user.verify_password(password):
            return user
        return False

    #W ktorym momencie hashowac?
    def create_user(self, Username: str, Email: str, Password: str):
        #new_User = User(username=Username, email=Email, password=Password)
        new_User = User(username=Username, email=Email, role="NEW_USER")
        new_User.set_password(Password)
        self.db.add(new_User)
        self.db.commit()
        self.db.refresh(new_User)
        return new_User






#USerLogin, Userservices nie dotykać models
##Nie robić asynchronicznie