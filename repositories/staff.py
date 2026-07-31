from sqlalchemy.orm import Session
from uuid import UUID
from models.staff import InstitutionStaff

class InstitutionStaffRepository:
    def __init__(self):
        self.model = InstitutionStaff

    def get(self, db: Session, staff_id: UUID):
        return db.get(InstitutionStaff, staff_id)
    
    def get_by_email(self, db: Session, email: str):
        return db.query(InstitutionStaff).filter(InstitutionStaff.email == email).first()
    
    def get_all(self, db: Session):
        return db.query(InstitutionStaff).all()

    def create(self, db: Session, data: dict):
        staff = InstitutionStaff(**data)
        db.add(staff)
        db.commit()
        db.refresh(staff)
        return staff

    def update(self, db: Session, db_obj: InstitutionStaff, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: InstitutionStaff):
        db.delete(db_obj)
        db.commit()

staff_repository = InstitutionStaffRepository()
