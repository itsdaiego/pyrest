from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
  username: str
  email: EmailStr

class UserResponse(UserBase):
    id: str

class UserCreate(UserBase):
    email: EmailStr
    password: str


class Login(BaseModel):
  username: str
  password: str


class Token(BaseModel):
  access_token: str
  refresh_token: str
