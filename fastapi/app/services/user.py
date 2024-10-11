import os

from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.models import User
from app.schemas.user import Token, UserCreate, UserResponse

SECRET_KEY = os.environ.get("SECRET") or "JUST_A_TEST"

if not SECRET_KEY:
    raise Exception("Missing SECRET environment variable")

ALGORITHM = "HS256"

bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserAlreadyExists(Exception):
    pass

class IncorrectCredentials(Exception):
    pass

class UserService:
    @staticmethod
    def create_access_token(user_uuid: str):
        return jwt.encode(
            { 
                "sub": user_uuid,
                "exp": datetime.utcnow() + timedelta(minutes=60)
            },
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    @staticmethod
    def create_refresh_token(user_uuid: str):
        return jwt.encode(
            { 
                "sub": user_uuid,
                "exp": datetime.utcnow() + timedelta(minutes=60)
            },
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    @staticmethod
    def register_user(user: UserCreate, db: Session) -> UserResponse:
        db_user = db.query(User).filter(User.email == user.email).first()

        if db_user:
            raise UserAlreadyExists()

        hashed_password = bcrypt.hash(user.password)

        db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
        db.add(db_user)

        db.commit()
        db.refresh(db_user)


        return UserResponse(
            id=str(db_user.id),
            username=str(db_user.username),
            email=EmailStr(db_user.email)
        )

    @staticmethod
    def authenticate_user(username: str, password: str, db: Session) -> Token:
        user = db.query(User).filter(User.username == username).first()

        if not user or not bcrypt.verify(password, str(user.hashed_password)):
            raise IncorrectCredentials()

        return Token(
            access_token=UserService.create_access_token(str(user.id)),
            refresh_token=UserService.create_refresh_token(str(user.id))
        )

    @staticmethod
    def get_user_by_username(username: str, db: Session) -> User:
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
