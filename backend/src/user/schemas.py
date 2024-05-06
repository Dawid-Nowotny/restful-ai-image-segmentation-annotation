from pydantic import BaseModel;

class UserCreateSchema(BaseModel):
    Username: str
    Email: str
    Password: str

class LoginInfo(BaseModel):
    Username: str
    Password: str