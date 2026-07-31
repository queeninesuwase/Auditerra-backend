
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from schemas.farmer import FarmerCreate, FarmerRead, FarmerUpdate
from services import farmer_service

router = APIRouter(prefix="/farmers", tags=["farmers"])


@router.get("/", response_model=list[FarmerRead])
def list_farmers(db: Session = Depends(get_db)):
    return farmer_service.list_farmers(db)


@router.get("/{farmer_id}", response_model=FarmerRead)
def get_farmer(farmer_id: UUID, db: Session = Depends(get_db)):
    return farmer_service.get_farmer(db, farmer_id)


@router.post("/", response_model=FarmerRead, status_code=status.HTTP_201_CREATED)
def create_farmer(data: FarmerCreate, db: Session = Depends(get_db)):
    return farmer_service.create_farmer(db, data)


@router.put("/{farmer_id}", response_model=FarmerRead)
def update_farmer(farmer_id: UUID, data: FarmerUpdate, db: Session = Depends(get_db)):
    return farmer_service.update_farmer(db, farmer_id, data)


@router.delete("/{farmer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_farmer(farmer_id: UUID, db: Session = Depends(get_db)):
    farmer_service.delete_farmer(db, farmer_id)
    return None


@router.post("/{farmer_id}/report-issue", status_code=status.HTTP_201_CREATED)
def report_issue(
    farmer_id: UUID,
    issue_category: str,
    description: str,
    db: Session = Depends(get_db)
):
    return farmer_service.report_issue(db, farmer_id, issue_category, description)


@router.get("/{farmer_id}/tickets")
def get_farmer_tickets(farmer_id: UUID, db: Session = Depends(get_db)):
    return farmer_service.get_farmer_tickets(db, farmer_id)


@router.post("/{farmer_id}/tickets/{ticket_id}/cancel")
def cancel_farmer_ticket(farmer_id: UUID, ticket_id: UUID, db: Session = Depends(get_db)):
    return farmer_service.cancel_farmer_ticket(db, farmer_id, ticket_id)


@router.post("/{farmer_id}/rotate-handshake")
def rotate_handshake(farmer_id: UUID, db: Session = Depends(get_db)):
    return farmer_service.rotate_handshake_for_visit(db, farmer_id)


@router.post("/{farmer_id}/verify-handshake")
def verify_handshake(farmer_id: UUID, code: str, db: Session = Depends(get_db)):
    return farmer_service.verify_handshake(db, farmer_id, code)