import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt

from app.models import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService, UserAlreadyExists, IncorrectCredentials, SECRET_KEY, ALGORITHM

def register_user(user_data: UserCreate, db: Session):
    try:
        return UserService.register_user(user_data, db)
    except UserAlreadyExists as e:
        logging.error("User already exists %s", user_data.email)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User already exists",
        )
    except Exception as e:
        logging.error("Error registering user %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )

def authenticate_user(username: str, password: str, db: Session):
    try:
        return UserService.authenticate_user(username, password, db)
    except IncorrectCredentials as e:
        logging.error("Incorrect credentials %s", username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
        )
    except Exception as e:
        logging.error("Error logging in %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )

def get_current_user(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        if user_id is None or user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not find user",
            )
        return user
    except Exception as e:
        logging.error("Error getting user %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )
