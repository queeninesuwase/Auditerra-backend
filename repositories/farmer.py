
from sqlalchemy.orm import Session
from uuid import UUID
from models.farmer import Farmer


class FarmerRepository:
    def __init__(self):
        self.model = Farmer

    def get(self, db: Session, farmer_id: UUID):
        return db.get(Farmer, farmer_id)

    def get_by_phone(self, db: Session, phone: str):
        return db.query(Farmer).filter(Farmer.phone == phone).first()

    def get_by_handshake(self, db: Session, code: str):
        return db.query(Farmer).filter(Farmer.unique_handshake_code == code).first()

    def get_all(self, db: Session):
        return db.query(Farmer).all()

    def create(self, db: Session, data: dict):
        farmer = Farmer(**data)
        db.add(farmer)
        db.commit()
        db.refresh(farmer)
        return farmer

    def update(self, db: Session, db_obj: Farmer, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Farmer):
        db.delete(db_obj)
        db.commit()


farmer_repository = FarmerRepository()