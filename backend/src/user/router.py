#endpointy
from urllib.request import Request

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .service import UserService
from .schemas import UserCreateSchema, LoginInfo

from get_db import get_db
#from backend.src.models import User


#from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
def login(login_info: LoginInfo, db: Session = Depends(get_db)):
    print(login_info.Username)
    print(login_info.Password)
    service = UserService(db)
    #print("test1")
    user = service.authenticate_user(login_info.Username, login_info.Password)
    #print("test2")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #raise HTTPException(status_code=status.HTTP_200_OK, detail="Login successful")
    return {"access_token": user.username}

#@router.post("/login")
#def login(Username: str, Password: str, db: Session = Depends(get_db)):
#    print("test1")
#    print(Username)
#    print(Password)
#    print("test2")
#    service = UserService(db)
#    user = service.authenticate_user(Username, Password)
#    if not user:
#        raise HTTPException(
#            status_code=status.HTTP_401_UNAUTHORIZED,
#            detail="Incorrect username or password",
#            headers={"WWW-Authenticate": "Bearer"},
#        )
#    return {"access_token": user.username, "token_type": "bearer"}

#async def login(username: str, password: str, db: Session = Depends(get_db)):
#    user = await authenticate_user(db, username, password)
#    if not user:
#        raise HTTPException(
#            status_code=status.HTTP_401_UNAUTHORIZED,
#            detail="Incorrect username or password",
#            headers={"WWW-Authenticate": "Bearer"},
#        )
#    return {"access_token": user.username, "token_type": "bearer"}


# response_model=UserCreateSchema,
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreateSchema, db: Session = Depends(get_db)):
    service = UserService(db)
    if service.check_if_user_exists(user.Username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    #czy uzyc usera z models?
    new_user = service.create_user(user.Username, user.Email, user.Password)
    return {
        "username": new_user.username,
        "email": new_user.email,
    }



#async def register(user: userCreateSchema, db: Session = Depends(get_db)):
#    existing_user = await User.get_user(db, user.username)
#    if existing_user:
#        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
#    new_user = await user.create_user(db, userCreateSchema)
#    return new_user

#
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#@router.get("/login/")
#async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#    user = await authenticate_user(db, form_data.username, form_data.password)
#    if not user:
#        raise HTTPException(
#            status_code=status.HTTP_401_UNAUTHORIZED,
#            detail="Incorrect username or password",
#            headers={"WWW-Authenticate": "Bearer"},
#        )
#    return {"access_token": user.username, "token_type": "bearer"}


#async def root():
#    return {"message": "Hello Login"}