
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

from repositories.ticket import ticket_repository
from repositories.farmer import farmer_repository
from repositories.staff import staff_repository
from schemas.ticket import ServiceTicketCreate, ServiceTicketUpdate


VALID_STATUS_TRANSITIONS = {
    "pending": {"dispatched", "cancelled"},
    "dispatched": {"resolved", "cancelled"},
    "cancelled": set(),
    "resolved": set(),
}


def get_ticket(db: Session, ticket_id: UUID):
    ticket = ticket_repository.get(db, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service request ticket not found"
        )
    return ticket


def list_tickets(db: Session):
    return ticket_repository.get_all(db)


def get_tickets_by_farmer(db: Session, farmer_id: UUID):
    return ticket_repository.get_by_farmer(db, farmer_id)


def get_tickets_by_expert(db: Session, staff_id: UUID):
    return ticket_repository.get_by_staff(db, staff_id)


def get_tickets_by_status(db: Session, status: str):
    if status not in VALID_STATUS_TRANSITIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket status filter"
        )
    return ticket_repository.get_by_status(db, status)


def create_ticket(db: Session, data: ServiceTicketCreate):
    farmer = farmer_repository.get(db, data.farmer_id)
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot open ticket: Linked farmer account profile not found"
        )
    payload = data.model_dump()
    payload["status"] = "pending"
    payload["staff_id"] = None
    return ticket_repository.create(db, payload)


def update_ticket(db: Session, ticket_id: UUID, data: ServiceTicketUpdate):
    ticket = get_ticket(db, ticket_id)
    payload = data.model_dump(exclude_unset=True)
    if "status" in payload:
        _validate_status_transition(ticket.status, payload["status"])
    return ticket_repository.update(db, ticket, payload)


def assign_expert(db: Session, ticket_id: UUID, staff_id: UUID):
    ticket = get_ticket(db, ticket_id)
    if ticket.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot assign expert to a ticket with status '{ticket.status}'"
        )
    expert = staff_repository.get(db, staff_id)
    if not expert:
        raise HTTPException(status_code=404, detail="Expert not found")
    if expert.role != "field_expert":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assigned staff member must be a field expert"
        )
    return ticket_repository.update(db, ticket, {
        "staff_id": staff_id,
        "status": "dispatched"
    })


def farmer_cancel_ticket(db: Session, ticket_id: UUID, farmer_id: UUID):
    ticket = get_ticket(db, ticket_id)
    if ticket.farmer_id != farmer_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    _validate_status_transition(ticket.status, "cancelled")
    return ticket_repository.update(db, ticket, {"status": "cancelled"})


def expert_resolve_ticket(db: Session, ticket_id: UUID, staff_id: UUID):
    ticket = get_ticket(db, ticket_id)
    if ticket.staff_id != staff_id:
        raise HTTPException(status_code=403, detail="Not authorized to resolve this ticket")
    _validate_status_transition(ticket.status, "resolved")
    return ticket_repository.update(db, ticket, {"status": "resolved"})


def delete_ticket(db: Session, ticket_id: UUID):
    ticket = get_ticket(db, ticket_id)
    ticket_repository.delete(db, ticket)


def _validate_status_transition(current: str, next_status: str):
    allowed = VALID_STATUS_TRANSITIONS.get(current, set())
    if next_status not in allowed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Invalid status transition from '{current}' to '{next_status}'"
        )