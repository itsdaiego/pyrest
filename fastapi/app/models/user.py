from enum import Enum

from sqlalchemy import Column, String, Enum as SQLAlchemyEnum
from app.db.database import Base
import uuid

class Profile(Enum):
    CLIENT = "client"
    CONTRACTOR = "contractor"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    profile = Column(SQLAlchemyEnum(Profile), default=Profile.CLIENT)

