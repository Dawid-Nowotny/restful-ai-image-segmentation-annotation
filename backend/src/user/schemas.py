from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class UserCreateSchema(BaseModel):
    username: str = Field(min_length=4,max_length=20)
    email: EmailStr
    password: str = Field(min_length=6,max_length=32)

class UserUpdateSchema(UserCreateSchema):
    username: Optional[str] = Field(None, min_length=4,max_length=20)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=32)
    old_password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    totp_enabled: bool

    model_config = ConfigDict(from_attributes=True)
        
class TokenData(BaseModel):
    username: str | None = None

class VerifyTotpRequest(BaseModel):
    token: str

class DisableTOTPRequest(BaseModel):
    password: str