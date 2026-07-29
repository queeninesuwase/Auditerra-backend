from sqlalchemy.orm import Session
from uuid import UUID
from models.expert import FieldExpert

class FieldExpertRepository:
    def __init__(self):
        self.model = FieldExpert

    def get(self, db: Session, expert_id: UUID):
        return db.get(FieldExpert, expert_id)
    
    def get_by_email(self, db: Session, email: str):
        return db.query(FieldExpert).filter(FieldExpert.email == email).first()
    
    def get_all(self, db: Session):
        return db.query(FieldExpert).all()

    def create(self, db: Session, data: dict):
        expert = FieldExpert(**data)
        db.add(expert)
        db.commit()
        db.refresh(expert)
        return expert

    def update(self, db: Session, db_obj: FieldExpert, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: FieldExpert):
        db.delete(db_obj)
        db.commit()

expert_repository = FieldExpertRepository()
