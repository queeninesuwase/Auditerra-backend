
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID
import random

from repositories.farmer import farmer_repository
from repositories.user import user_repository
from repositories.ticket import ticket_repository
from schemas.farmer import FarmerCreate, FarmerUpdate
from schemas.ticket import ServiceTicketCreate


def get_farmer(db: Session, farmer_id: UUID):
    farmer = farmer_repository.get(db, farmer_id)
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer profile not found"
        )
    return farmer


def get_farmer_by_phone(db: Session, phone: str):
    user = user_repository.get_by_phone(db, phone)
    if not user or user.role != "farmer":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No farmer registered with this phone number"
        )
    return farmer_repository.get(db, user.user_id)


def list_farmers(db: Session):
    return farmer_repository.get_all(db)


def create_farmer(db: Session, data: FarmerCreate):
    existing = user_repository.get_by_phone(db, data.phone)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this phone number is already registered"
        )

    user_data = {
        "name": data.name,
        "phone": data.phone,
        "county": data.county,
        "preferred_language": data.preferred_language,
        "role": "farmer"
    }
    user = user_repository.create(db, user_data)

    farmer_data = {
        "farmer_id": user.user_id,
        "unique_handshake_code": _generate_unique_handshake(db),
        "sub_county": data.sub_county,
        "village": data.village,
        "landmark": data.landmark
    }
    return farmer_repository.create(db, farmer_data)


def update_farmer(db: Session, farmer_id: UUID, data: FarmerUpdate):
    farmer = get_farmer(db, farmer_id)
    user_updates = {}
    profile_updates = {}

    for field, value in data.model_dump(exclude_unset=True).items():
        if field in ("name", "phone", "county", "preferred_language"):
            user_updates[field] = value
        else:
            profile_updates[field] = value

    if user_updates:
        user_repository.update(db, farmer.user, user_updates)
    if profile_updates:
        farmer_repository.update(db, farmer, profile_updates)

    db.refresh(farmer)
    return farmer


def delete_farmer(db: Session, farmer_id: UUID):
    farmer = get_farmer(db, farmer_id)
    user = farmer.user
    farmer_repository.delete(db, farmer)
    if user:
        user_repository.delete(db, user)


def report_issue(db: Session, farmer_id: UUID, issue_category: str, description: str):
    farmer = get_farmer(db, farmer_id)

    ticket_data = ServiceTicketCreate(
        farmer_id=farmer_id,
        issue_category=issue_category,
        description=description
    )

    payload = ticket_data.model_dump()
    payload["status"] = "pending"
    payload["staff_id"] = None

    ticket = ticket_repository.create(db, payload)

    new_handshake = _generate_unique_handshake(db)
    farmer_repository.update(db, farmer, {"unique_handshake_code": new_handshake})

    return {
        "ticket_id": ticket.ticket_id,
        "status": ticket.status,
        "handshake_code": new_handshake,
        "message": "Issue reported. Wait for SMS with expert details and arrival time."
    }


def get_farmer_tickets(db: Session, farmer_id: UUID):
    farmer = get_farmer(db, farmer_id)
    tickets = ticket_repository.get_by_farmer(db, farmer_id)
    result = []
    for ticket in tickets:
        expert = None
        if ticket.staff_id:
            from repositories.staff import staff_repository
            expert = staff_repository.get(db, ticket.staff_id)
        result.append({
            "ticket_id": ticket.ticket_id,
            "issue_category": ticket.issue_category,
            "status": ticket.status,
            "description": ticket.description,
            "expert_name": expert.name if expert else None,
            "expert_phone": expert.phone if expert else None,
            "created_at": ticket.created_at
        })
    return result


def cancel_farmer_ticket(db: Session, farmer_id: UUID, ticket_id: UUID):
    farmer = get_farmer(db, farmer_id)
    ticket = ticket_repository.get(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.farmer_id != farmer_id:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this ticket")
    if ticket.status not in ("pending", "dispatched"):
        raise HTTPException(status_code=409, detail="Cannot cancel ticket in current state")

    ticket_repository.update(db, ticket, {"status": "cancelled"})
    return {"ticket_id": ticket_id, "status": "cancelled"}


def rotate_handshake_for_visit(db: Session, farmer_id: UUID):
    farmer = get_farmer(db, farmer_id)
    new_code = _generate_unique_handshake(db)
    farmer_repository.update(db, farmer, {"unique_handshake_code": new_code})
    return {"farmer_id": farmer_id, "new_handshake_code": new_code}


def verify_handshake(db: Session, farmer_id: UUID, code: str) -> bool:
    farmer = get_farmer(db, farmer_id)
    if farmer.unique_handshake_code != code:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid security handshake code"
        )
    return True


def _generate_unique_handshake(db: Session, max_retries: int = 10) -> str:
    for _ in range(max_retries):
        code = f"{random.randint(0, 9999):04d}"
        existing = farmer_repository.get_by_handshake(db, code)
        if not existing:
            return code
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unable to generate a unique handshake code"
    )