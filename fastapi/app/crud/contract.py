import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from app.schemas.contract import ContractCreate, ContractResponse
from app.services.contract import ContractService

def create_contract(contract: ContractCreate, db: Session) -> ContractResponse:
    try:
        return ContractService.create_contract(contract, db)
    except Exception as e:
        logging.error("Service failed", contract)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
