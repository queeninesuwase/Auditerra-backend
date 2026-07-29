from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

from repositories.ticket import ticket_repository
from repositories.farmer import farmer_repository
from schemas.ticket import ServiceTicketCreate, ServiceTicketUpdate

def get_ticket(db: Session, ticket_id: UUID):
    ticket = ticket_repository.get(db, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Service ticket record not found"
        )
    return ticket

def list_tickets(db: Session):
    return ticket_repository.get_all(db)

def create_ticket(db: Session, data: ServiceTicketCreate):

    farmer = farmer_repository.get(db, data.farmer_id)
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot open ticket: Farmer account profile not found"
        )
        
    payload = data.model_dump()
    payload["status"] = "pending" 
    return ticket_repository.create(db, payload)

def update_ticket(db: Session, ticket_id: UUID, data: ServiceTicketUpdate):
    ticket = get_ticket(db, ticket_id)
    return ticket_repository.update(db, ticket, data.model_dump(exclude_unset=True))

def delete_ticket(db: Session, ticket_id: UUID):
    ticket = get_ticket(db, ticket_id)
    ticket_repository.delete(db, ticket)
