from sqlalchemy.orm import Session
from uuid import UUID
from models.location import Location

class LocationRepository:
    def __init__(self):
        self.model = Location

    def get(self, db: Session, location_id: UUID):
        return db.get(Location, location_id)
    
    def get_all(self, db: Session):
        return db.query(Location).all()

    def create(self, db: Session, data: dict):
        location = Location(**data)
        db.add(location)
        db.commit()
        db.refresh(location)
        return location

    def update(self, db: Session, db_obj: Location, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Location):
        db.delete(db_obj)
        db.commit()

location_repository = LocationRepository()
