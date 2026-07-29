from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

from repositories.supervisor import supervisor_repository
from schemas.supervisor import InstitutionalSupervisorCreate, InstitutionalSupervisorUpdate

def get_supervisor(db: Session, supervisor_id: UUID):
    supervisor = supervisor_repository.get(db, supervisor_id)
    if not supervisor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Institutional supervisor not found"
        )
    return supervisor

def list_supervisors(db: Session):
    return supervisor_repository.get_all(db)

def create_supervisor(db: Session, data: InstitutionalSupervisorCreate):
    existing = supervisor_repository.get_by_email(db, data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A supervisor with this email is already registered"
        )
        
    payload = data.model_dump()
    raw_password = payload.pop("password")
    payload["password_hash"] = f"hashed_{raw_password}"
    
    return supervisor_repository.create(db, payload)

def update_supervisor(db: Session, supervisor_id: UUID, data: InstitutionalSupervisorUpdate):
    supervisor = get_supervisor(db, supervisor_id)
    return supervisor_repository.update(db, supervisor, data.model_dump(exclude_unset=True))

def delete_supervisor(db: Session, supervisor_id: UUID):
    supervisor = get_supervisor(db, supervisor_id)
    supervisor_repository.delete(db, supervisor)
