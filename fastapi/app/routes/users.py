import logging

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.helpers.authenticate import user_is_authenticated
from app.schemas.user import Login, Token, UserCreate, UserResponse
from app.services.user import IncorrectCredentials, UserAlreadyExists, UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter()

@auth_router.post("/register", response_model=UserResponse)
def register(json_data: UserCreate = Body(...), db: Session = Depends(get_db)):
    try:
        return UserService.register_user(json_data, db)
    except UserAlreadyExists as e:
        logging.error(f"User already exists: {json_data.email}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User already exists",
        )
    except Exception as e:
        logging.error(f"Error registering user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )


@auth_router.post("/login", response_model=Token)
def login(json_data: Login = Body(...), db: Session = Depends(get_db)):
    try:
        return UserService.authenticate_user(json_data.username, json_data.password, db)
    except IncorrectCredentials as e:
        logging.error(f"Incorrect credentials: {json_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
        )
    except Exception as e:
        logging.error(f"Error logging in: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )

user_router = APIRouter()

@user_router.get("/me", response_model=UserResponse, dependencies=[Depends(user_is_authenticated)])
def users_me(user: UserResponse = Depends(user_is_authenticated)):
    try:
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            profile=user.profile
        )
    except Exception as e:
        logging.error(f"Error getting current user: {str(e)}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )

