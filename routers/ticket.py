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

@router.get("/{ticket_id}", response_model=ServiceTicketRead)
def get_ticket(ticket_id: UUID, db: Session = Depends(get_db)):
    return ticket_service.get_ticket(db, ticket_id)

@router.post("/", response_model=ServiceTicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(data: ServiceTicketCreate, db: Session = Depends(get_db)):
    return ticket_service.create_ticket(db, data)

@router.put("/{ticket_id}", response_model=ServiceTicketRead)
def update_ticket(ticket_id: UUID, data: ServiceTicketUpdate, db: Session = Depends(get_db)):
    return ticket_service.update_ticket(db, ticket_id, data)

@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: UUID, db: Session = Depends(get_db)):
    ticket_service.delete_ticket(db, ticket_id)
    return None
