from pydantic import BaseModel, EmailStr, Field

class UserCreateSchema(BaseModel):
    username: str = Field(min_length=4,max_length=20)
    email: EmailStr
    password: str = Field(min_length=6,max_length=32)

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    totp_enabled: bool

class TokenData(BaseModel):
    username: str | None = None