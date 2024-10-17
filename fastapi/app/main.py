from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.routes import user_routes, auth_routes, contract_routes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

app.include_router(user_routes, prefix="/users", tags=["users"])
app.include_router(auth_routes, prefix='/auth', tags=["auth"])
app.include_router(contract_routes, prefix='/contracts', tags=["contracts"])
