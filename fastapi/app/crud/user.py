import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request, status
from jose import jwt

from app.models import User
from app.schemas.user import UserCreate
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

def get_current_user(request: Request):
    try:
        return request.state.user
    except Exception as e:
        logging.error("Error getting user %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )
