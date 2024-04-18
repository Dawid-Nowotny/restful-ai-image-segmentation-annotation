from pydantic import BaseModel

class UserSchema(BaseModel):
  user_id: int
  username: str
  email: str
  passwordHash: str
  role: str
