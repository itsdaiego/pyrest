from sqlalchemy.orm import Session
from app.models.contract import Contract, ContractStatus
from app.models.job import Job
from app.schemas.job import JobPaymentCreate, JobResponse

class ContractNotFound(Exception):
    pass

class JobNotFound(Exception):
    pass

class JobService:
    @staticmethod
    def process_payment(payment_data: JobPaymentCreate, db: Session):
        job = db.query(Job).filter(Job.id == payment_data.job_id).first()

        if not job:
            raise JobNotFound()

        contract = db.query(Contract).filter(Contract.id == job.contract).first()

        if not contract:
            raise ContractNotFound()

        job.paid = True
        job.payment_date = payment_data.payment_date

        db.commit()
        db.refresh(job)
        db.refresh(contract)

        return JobResponse(
            id=job.id,
            description=job.description,
            price=job.price,
            paid=job.paid,
            payment_date=job.payment_date,
            contract=job.contract
        )
