from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

from repositories.log import log_repository
from schemas.log import DiagnosticLogCreate, DiagnosticLogUpdate

def get_log(db: Session, log_id: UUID):
    log = log_repository.get(db, log_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Soil diagnostic logging entry not found"
        )
    return log

def list_logs(db: Session):
    return log_repository.get_all(db)

def create_log(db: Session, data: DiagnosticLogCreate):
    if data.ticket_id:
        existing = log_repository.get_by_ticket(db, data.ticket_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A soil assessment diagnostic log has already been submitted for this ticket record"
            )
    return log_repository.create(db, data.model_dump())

def update_log(db: Session, log_id: UUID, data: DiagnosticLogUpdate):
    log = get_log(db, log_id)
    return log_repository.update(db, log, data.model_dump(exclude_unset=True))

def delete_log(db: Session, log_id: UUID):
    log = get_log(db, log_id)
    log_repository.delete(db, log)
