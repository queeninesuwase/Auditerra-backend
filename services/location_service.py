from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

from repositories.location import location_repository
from schemas.location import LocationCreate, LocationUpdate

def get_location(db: Session, location_id: UUID):
    location = location_repository.get(db, location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Location coordinate entry not found"
        )
    return location

def list_locations(db: Session):
    return location_repository.get_all(db)

def create_location(db: Session, data: LocationCreate):
    return location_repository.create(db, data.model_dump())

def update_location(db: Session, location_id: UUID, data: LocationUpdate):
    location = get_location(db, location_id)
    return location_repository.update(db, location, data.model_dump(exclude_unset=True))

def delete_location(db: Session, location_id: UUID):
    location = get_location(db, location_id)
    location_repository.delete(db, location)
