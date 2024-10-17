from pydantic import BaseModel, EmailStr

from app.models.user import Profile

class UserBase(BaseModel):
  username: str
  email: EmailStr

class UserResponse(UserBase):
    id: str
    profile: Profile

class UserCreate(UserBase):
    email: EmailStr
    password: str


class Login(BaseModel):
  username: str
  password: str


class Token(BaseModel):
  access_token: str
  refresh_token: str
