

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from app.db.database import Base


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    paid = Column(Boolean, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    contract = Column(Integer, ForeignKey('contracts.id'))
