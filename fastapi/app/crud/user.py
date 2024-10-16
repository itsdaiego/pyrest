import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.user import Token, UserCreate, UserResponse
from app.services.user import UserService, UserAlreadyExists, IncorrectCredentials


def register_user(user_data: UserCreate, db: Session) -> UserResponse:
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


def authenticate_user(username: str, password: str, db: Session) -> Token:
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

