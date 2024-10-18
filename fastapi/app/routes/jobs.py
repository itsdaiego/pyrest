import logging

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from app.db.database import get_db
from app.schemas.job import JobPaymentCreate, JobPaymentResponse
from app.services.job import ContractNotFound, JobNotFound, JobService

router = APIRouter()

@router.post("/process_payment", response_model=JobPaymentResponse)
def process_payment(payment_data: JobPaymentCreate = Body(...), db: Session = Depends(get_db)):
    try:
        return JobService.process_payment(payment_data, db)
    except JobNotFound:
        logging.error("Job not found")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Job not found")
    except ContractNotFound:
        logging.error("Contract not found")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Contract not found")
    except Exception as e:
        logging.error(f"Internal server error: {str(e)}")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
