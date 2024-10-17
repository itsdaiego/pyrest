from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from enum import Enum

class ContractStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    status = Column(SQLAlchemyEnum(ContractStatus), default=ContractStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client_id = Column(String, ForeignKey("users.id"))
    client = relationship("User", foreign_keys=[client_id])

    contractor_id = Column(String, ForeignKey("users.id"))
    contractor = relationship("User", foreign_keys=[contractor_id])
