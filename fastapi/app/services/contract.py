from sqlalchemy.orm import Session
from app.models.contract import Contract, ContractStatus
from app.schemas.contract import ContractCreate, ContractResponse
from datetime import datetime


class ContractService:
    @staticmethod
    def create_contract(contract: ContractCreate, db: Session) -> ContractResponse:
        try:
            db_contract = Contract(
                title=contract.title,
                description=contract.description,
                price=contract.price,
                client_id=contract.client_id,
                contractor_id=contract.contractor_id,
                status=ContractStatus.PENDING
            )

            db.add(db_contract)
            db.commit()
            db.refresh(db_contract)

            return ContractResponse(
                id=db_contract.id,
                title=db_contract.title,
                description=db_contract.description,
                price=db_contract.price,
                client_id=db_contract.client_id,
                contractor_id=db_contract.contractor_id,
                created_at=db_contract.created_at,
                updated_at=db_contract.updated_at,
                status=db_contract.status
            )
        except Exception as e:
            db.rollback()
            raise e
