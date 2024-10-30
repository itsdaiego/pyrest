
import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from ..db.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] =  mapped_column(primary_key=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    paid: Mapped[bool] = mapped_column(Boolean, nullable=False)
    payment_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    contract: Mapped[int] = mapped_column(Integer, ForeignKey('contracts.id'))

    class Config:
        orm_mode = True
