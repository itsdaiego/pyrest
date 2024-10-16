from fastapi import FastAPI, Request, HTTPException, Depends
from jose import jwt, JWTError
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session


app = FastAPI()


async def user_is_authenticated(request: Request, db: Session = Depends(get_db)) -> UserResponse:
    bearer_token = request.headers.get("Authorization")

    if not bearer_token:
        raise HTTPException(status_code=401, detail="No token provided")

    try:
        print("Hello")
        token = bearer_token.split("Bearer ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        print("User is authenticated", user.email)

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid token format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
