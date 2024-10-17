from pydantic import BaseModel
from datetime import datetime

from pydantic.types import UUID4 as UUID

from app.models.contract import ContractStatus

class ContractBase(BaseModel):
    title: str
    description: str
    price: float
    client_id: UUID
    contractor_id: UUID

class ContractCreate(ContractBase):
    pass

class ContractResponse(ContractBase):
    id: int
    title: str
    description: str
    price: float
    created_at: datetime
    updated_at: datetime
    status: ContractStatus
    client_id: UUID
    contractor_id: UUID


    class Config:
        orm_mode = True
