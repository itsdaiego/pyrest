from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserResponse, UserCreate, Token, Login
from app.crud import user as user_crud

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/me", response_model=UserResponse)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return user_crud.get_current_user(token, db)

auth_router = APIRouter()

@auth_router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate = Body(...), db: Session = Depends(get_db)):
    return user_crud.register_user(user_data, db)

@auth_router.post("/login", response_model=Token)
def login(login_data: Login = Body(...), db: Session = Depends(get_db)):
    return user_crud.authenticate_user(login_data.username, login_data.password, db)

