import logging

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_422_UNPROCESSABLE_ENTITY
from app.db.database import get_db
from app.schemas.contract import ContractCreate, ContractResponse
from app.services.contract import ContractDuplicatedProfile, ContractMissingProfile, ContractService

router = APIRouter()

@router.post("/")
# @router.post("/", response_model=ContractResponse)
def create_contract(json_data: ContractCreate = Body(...), db: Session = Depends(get_db)):
    try:
        return ContractService.create_contract(json_data, db)
    except ContractDuplicatedProfile:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Contractor and client have the same profile")
    except ContractMissingProfile:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Contractor or client profile is missing")
    except Exception as e:
        logging.error("Something went wrong while creating a contract %s", e)

        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
