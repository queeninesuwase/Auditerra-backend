from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

from repositories.staff import staff_repository
from schemas.staff import InstitutionStaffCreate, InstitutionStaffUpdate

def get_staff(db: Session, staff_id: UUID):
    staff = staff_repository.get(db, staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Institution staff member profile not found"
        )
    return staff

def list_staff(db: Session):
    return staff_repository.get_all(db)

def create_staff(db: Session, data: InstitutionStaffCreate):
    existing = staff_repository.get_by_email(db, data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A staff member with this email is already registered"
        )
    
    payload = data.model_dump()
    raw_password = payload.pop("password")
    
    payload["password_hash"] = f"hashed_{raw_password}"
    
    return staff_repository.create(db, payload)

def update_staff(db: Session, staff_id: UUID, data: InstitutionStaffUpdate):
    staff = get_staff(db, staff_id)
    return staff_repository.update(db, staff, data.model_dump(exclude_unset=True))

def delete_staff(db: Session, staff_id: UUID):
    staff = get_staff(db, staff_id)
    staff_repository.delete(db, staff)
