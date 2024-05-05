#modele w pydanic
from pydantic import BaseModel;


class UserCreateSchema(BaseModel):
    Username: str
    Email: str
    Password: str##dostajesz password nie pwd hash


class LoginInfo(BaseModel):
    Username: str
    Password: str
