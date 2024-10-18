from sqlalchemy.orm import Session
from app.models.contract import Contract
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobPaymentCreate, JobResponse

class ContractNotFound(Exception):
    pass

class JobNotFound(Exception):
    pass

class JobService:
    @staticmethod
    def process_payment(payment_data: JobPaymentCreate, db: Session):
        try:
            with db.begin():
                job = db.query(Job).filter(Job.id == payment_data.job_id).first()
            
                if not job:
                    raise JobNotFound()
            
                contract = db.query(Contract).filter(Contract.id == job.contract).first()
            
                if not contract:
                    raise ContractNotFound()
            
                job.paid = True
                job.payment_date = payment_data.payment_date

                client_profile = db.query(User).filter(User.id == contract.client.id).first()
                contractor_profile = db.query(User).filter(User.id == contract.contractor.id).first()

                client_profile.balance -= float(job.price)
                contractor_profile.balance += float(job.price)

            db.refresh(job)

            response = JobResponse(
                id=job.id,
                description=job.description,
                price=job.price,
                paid=job.paid,
                payment_date=job.payment_date,
                contract=job.contract
            )

            return response
        except Exception as e:
            if 'transaction' in locals():
                transaction.rollback()
            raise e
