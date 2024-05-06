from pydantic import BaseModel;

class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str

class LoginInfo(BaseModel):
    username: str
    password: str