import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from app.db.database import get_db
from app.models.user import User
from app.services.user import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session


app = FastAPI()


@app.middleware("http")
async def user_is_authenticated(request: Request, call_next):
    bearer_token = request.headers.get("Authorization")

    if not bearer_token:
        return JSONResponse(status_code=401, content={"error": "No token provided"})

    try:
        token = bearer_token.split("Bearer ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        db: Session = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        request.state.user = user

    except JWTError:
        return JSONResponse(status_code=401, content={"error": "Could not validate credentials"})
    except IndexError:
        return JSONResponse(status_code=401, content={"error": "Invalid token format"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"An error occurred: {str(e)}"})

    response = await call_next(request)
    return response
