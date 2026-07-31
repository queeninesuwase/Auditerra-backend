
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from schemas.ticket import ServiceTicketCreate, ServiceTicketRead, ServiceTicketUpdate
from services import ticket_service

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("/", response_model=list[ServiceTicketRead])
def list_tickets(db: Session = Depends(get_db)):
    return ticket_service.list_tickets(db)


@router.get("/status/{status}", response_model=list[ServiceTicketRead])
def get_by_status(status: str, db: Session = Depends(get_db)):
    return ticket_service.get_tickets_by_status(db, status)


@router.get("/farmer/{farmer_id}", response_model=list[ServiceTicketRead])
def get_by_farmer(farmer_id: UUID, db: Session = Depends(get_db)):
    return ticket_service.get_tickets_by_farmer(db, farmer_id)


@router.get("/expert/{staff_id}", response_model=list[ServiceTicketRead])
def get_by_expert(staff_id: UUID, db: Session = Depends(get_db)):
    return ticket_service.get_tickets_by_expert(db, staff_id)


@router.get("/{ticket_id}", response_model=ServiceTicketRead)
def get_ticket(ticket_id: UUID, db: Session = Depends(get_db)):
    return ticket_service.get_ticket(db, ticket_id)


@router.post("/", response_model=ServiceTicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(data: ServiceTicketCreate, db: Session = Depends(get_db)):
    return ticket_service.create_ticket(db, data)


@router.put("/{ticket_id}", response_model=ServiceTicketRead)
def update_ticket(ticket_id: UUID, data: ServiceTicketUpdate, db: Session = Depends(get_db)):
    return ticket_service.update_ticket(db, ticket_id, data)


@router.post("/{ticket_id}/assign-expert/{staff_id}", response_model=ServiceTicketRead)
def assign_expert(ticket_id: UUID, staff_id: UUID, db: Session = Depends(get_db)):
    return ticket_service.assign_expert(db, ticket_id, staff_id)


@router.post("/{ticket_id}/cancel/{farmer_id}", response_model=ServiceTicketRead)
def cancel_ticket(ticket_id: UUID, farmer_id: UUID, db: Session = Depends(get_db)):
    return ticket_service.farmer_cancel_ticket(db, ticket_id, farmer_id)


@router.post("/{ticket_id}/resolve/{staff_id}", response_model=ServiceTicketRead)
def resolve_ticket(ticket_id: UUID, staff_id: UUID, db: Session = Depends(get_db)):
    return ticket_service.expert_resolve_ticket(db, ticket_id, staff_id)


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: UUID, db: Session = Depends(get_db)):
    ticket_service.delete_ticket(db, ticket_id)
    return None