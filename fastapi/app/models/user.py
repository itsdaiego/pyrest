from enum import Enum

from sqlalchemy import Column, Float, String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base
import uuid

class Profile(Enum):
    CLIENT = "client"
    CONTRACTOR = "contractor"

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    profile: Mapped[Profile] = mapped_column(SQLAlchemyEnum(Profile), default=Profile.CLIENT)
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    # TODO: add timestamps (created_at, updated_at) to all models
