import logging

from fastapi import Body, FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
from app.db import get_db
from app.models import User
from app.schemas.user import UserCreate, UserResponse, Token
from app.schemas.user import Login
from app.services.user import IncorrectCredentials, UserAlreadyExists, UserService, SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload is None:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()


        if user_id is None or user is None:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not find user",
            )

        return user

    except Exception as e:
        logging.error("Error getting user", str(e))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )


@app.post("/register", response_model=Token)
def register(json_data: UserCreate = Body(...), db: Session = Depends(get_db)):
    try:
        return UserService.register_user(json_data, db)
    except UserAlreadyExists as e:
        logging.error("User already exists", json_data.email)

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User already exists",
        )
    except Exception as e:
        logging.error("Error registering user", str(e))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )



@app.post("/login", response_model=Token)
def login(json_data: Login = Body(...), db: Session = Depends(get_db)):
    try:
        UserService.authenticate_user(json_data.username, json_data.password, db)
    except IncorrectCredentials as e:
        logging.error("Incorrect credentials", json_data.username)

        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
        )
    except Exception as e:
        logging.error("Error logging in", str(e))

        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )


@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
