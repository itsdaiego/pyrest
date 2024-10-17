import logging

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from app.db.database import get_db
from app.schemas.contract import ContractCreate, ContractResponse
from app.crud import contract as contract_crud

router = APIRouter()

@router.post("/", response_model=ContractResponse)
def create_contract(json_data: ContractCreate = Body(...), db: Session = Depends(get_db)):
    try:
        return contract_crud.create_contract(json_data, db)
    except Exception as e:
        logging.error("Something went wrong while creating a contract %s", e)

        return HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
