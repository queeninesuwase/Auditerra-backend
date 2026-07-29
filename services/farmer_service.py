from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

from repositories.farmer import farmer_repository
from schemas.farmer import FarmerCreate, FarmerUpdate

def get_farmer(db: Session, farmer_id: UUID):
    farmer = farmer_repository.get(db, farmer_id)
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Farmer profile not found"
        )
    return farmer

def list_farmers(db: Session):
    return farmer_repository.get_all(db)

def create_farmer(db: Session, data: FarmerCreate):
    
    existing = farmer_repository.get_by_phone(db, data.phone)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A farmer with this phone number is already registered"
        )
    return farmer_repository.create(db, data.model_dump())

def update_farmer(db: Session, farmer_id: UUID, data: FarmerUpdate):
    farmer = get_farmer(db, farmer_id)
    return farmer_repository.update(db, farmer, data.model_dump(exclude_unset=True))

def delete_farmer(db: Session, farmer_id: UUID):
    
    farmer = get_farmer(db, farmer_id)
    farmer_repository.delete(db, farmer)
