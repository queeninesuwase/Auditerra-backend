from sqlalchemy.orm import Session
from uuid import UUID
from models.supervisor import InstitutionalSupervisor

class InstitutionalSupervisorRepository:
    def __init__(self):
        self.model = InstitutionalSupervisor

    def get(self, db: Session, supervisor_id: UUID):
        return db.get(InstitutionalSupervisor, supervisor_id)
    
    def get_by_email(self, db: Session, email: str):
        return db.query(InstitutionalSupervisor).filter(InstitutionalSupervisor.email == email).first()
    
    def get_all(self, db: Session):
        return db.query(InstitutionalSupervisor).all()

    def create(self, db: Session, data: dict):
        supervisor = InstitutionalSupervisor(**data)
        db.add(supervisor)
        db.commit()
        db.refresh(supervisor)
        return supervisor

    def update(self, db: Session, db_obj: InstitutionalSupervisor, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: InstitutionalSupervisor):
        db.delete(db_obj)
        db.commit()

supervisor_repository = InstitutionalSupervisorRepository()
