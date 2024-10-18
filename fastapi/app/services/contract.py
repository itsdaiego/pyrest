from sqlalchemy.orm import Session
from app.models.contract import Contract, ContractStatus
from app.models.user import User
from app.schemas.contract import ContractCreate, ContractResponse


class ContractDuplicatedProfile(Exception):
    pass

class ContractMissingProfile(Exception):
    pass


class ContractService:
    @staticmethod
    def create_contract(contract: ContractCreate, db: Session) -> ContractResponse:
        try:
            client_id = str(contract.client_id)
            contractor_id = str(contract.contractor_id)
            profile_client = db.query(User).filter(User.id == client_id).first()
            profile_contractor = db.query(User).filter(User.id == contractor_id).first()

            if not profile_client or not profile_contractor:
                raise Exception("Could not find user profiles")

            if not profile_client:
                raise ContractMissingProfile()

            if not profile_contractor:
                raise ContractMissingProfile()

            if profile_client.profile.value == profile_contractor.profile.value:
                raise ContractDuplicatedProfile()

            db_contract = Contract(
                title=contract.title,
                description=contract.description,
                price=contract.price,
                client_id=client_id,
                contractor_id=contractor_id,
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
