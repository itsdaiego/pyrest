from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class JobBase(BaseModel):
    description: str
    price: int

class JobCreate(JobBase):
    contract: int

class JobResponse(JobBase):
    id: int
    paid: bool
    payment_date: Optional[datetime]
    contract: int

    class Config:
        orm_mode = True

class JobPaymentCreate(BaseModel):
    job_id: int
    payment_date: datetime

class JobPaymentResponse(JobResponse):
    pass
