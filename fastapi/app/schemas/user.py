from pydantic import BaseModel, EmailStr

from app.models.user import Profile

class UserBase(BaseModel):
  username: str
  email: EmailStr
  profile: Profile

class UserResponse(UserBase):
    id: str

class UserCreate(UserBase):
    password: str


class Login(BaseModel):
  username: str
  password: str


class Token(BaseModel):
  access_token: str
  refresh_token: str
