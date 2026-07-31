
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from repositories.log import log_repository
from repositories.ticket import ticket_repository
from repositories.staff import staff_repository
from repositories.farmer import farmer_repository
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


def get_log_by_ticket(db: Session, ticket_id: UUID):
    log = log_repository.get_by_ticket(db, ticket_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No diagnostic log found for this ticket"
        )
    return log


def get_logs_by_expert(db: Session, staff_id: UUID):
    return log_repository.get_by_staff(db, staff_id)


def create_log(db: Session, data: DiagnosticLogCreate):
    ticket = ticket_repository.get(db, data.ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Linked service ticket not found"
        )
    if ticket.status != "dispatched":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot create diagnostic log for ticket with status '{ticket.status}'"
        )
    if data.ticket_id:
        existing = log_repository.get_by_ticket(db, data.ticket_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A soil assessment diagnostic log has already been submitted for this ticket record"
            )
    staff = staff_repository.get(db, data.staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Field expert not found")
    if staff.role != "field_expert":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Diagnostic logs can only be created by field experts"
        )
    if not data.location_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="GPS location is required for every diagnostic log"
        )

    farmer = farmer_repository.get(db, ticket.farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    return log_repository.create(db, data.model_dump())


def update_log(db: Session, log_id: UUID, data: DiagnosticLogUpdate):
    log = get_log(db, log_id)
    return log_repository.update(db, log, data.model_dump(exclude_unset=True))


def delete_log(db: Session, log_id: UUID):
    log = get_log(db, log_id)
    log_repository.delete(db, log)


def sync_offline_logs(db: Session, logs_data: List[DiagnosticLogCreate]):
    results = []
    for data in logs_data:
        existing = log_repository.get_by_ticket(db, data.ticket_id)
        if existing:
            results.append(existing)
        else:
            results.append(create_log(db, data))
    return results