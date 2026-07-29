from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from schemas.supervisor import InstitutionalSupervisorCreate, InstitutionalSupervisorRead, InstitutionalSupervisorUpdate
from services import supervisor_service

router = APIRouter(prefix="/supervisors", tags=["supervisors"])

@router.get("/", response_model=list[InstitutionalSupervisorRead])
def list_supervisors(db: Session = Depends(get_db)):
    return supervisor_service.list_supervisors(db)

@router.get("/{supervisor_id}", response_model=InstitutionalSupervisorRead)
def get_supervisor(supervisor_id: UUID, db: Session = Depends(get_db)):
    return supervisor_service.get_supervisor(db, supervisor_id)

@router.post("/", response_model=InstitutionalSupervisorRead, status_code=status.HTTP_201_CREATED)
def create_supervisor(data: InstitutionalSupervisorCreate, db: Session = Depends(get_db)):
    return supervisor_service.create_supervisor(db, data)

@router.put("/{supervisor_id}", response_model=InstitutionalSupervisorRead)
def update_supervisor(supervisor_id: UUID, data: InstitutionalSupervisorUpdate, db: Session = Depends(get_db)):
    return supervisor_service.update_supervisor(db, supervisor_id, data)

@router.delete("/{supervisor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supervisor(supervisor_id: UUID, db: Session = Depends(get_db)):
    supervisor_service.delete_supervisor(db, supervisor_id)
    return None
