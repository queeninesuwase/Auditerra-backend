from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from schemas.staff import InstitutionStaffCreate, InstitutionStaffRead, InstitutionStaffUpdate
from services import staff_service

router = APIRouter(prefix="/staff", tags=["institution-staff"])

@router.get("/", response_model=list[InstitutionStaffRead])
def list_staff(db: Session = Depends(get_db)):
    return staff_service.list_staff(db)

@router.get("/{staff_id}", response_model=InstitutionStaffRead)
def get_staff(staff_id: UUID, db: Session = Depends(get_db)):
    return staff_service.get_staff(db, staff_id)

@router.post("/", response_model=InstitutionStaffRead, status_code=status.HTTP_201_CREATED)
def create_staff(data: InstitutionStaffCreate, db: Session = Depends(get_db)):
    return staff_service.create_staff(db, data)

@router.put("/{staff_id}", response_model=InstitutionStaffRead)
def update_staff(staff_id: UUID, data: InstitutionStaffUpdate, db: Session = Depends(get_db)):
    return staff_service.update_staff(db, staff_id, data)

@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(staff_id: UUID, db: Session = Depends(get_db)):
    staff_service.delete_staff(db, staff_id)
    return None
