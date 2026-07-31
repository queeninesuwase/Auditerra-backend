
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from database import get_db
from services import dispatch_service

router = APIRouter(prefix="/dispatch", tags=["dispatch"])


@router.post("/ticket/{ticket_id}")
def dispatch_expert(
    ticket_id: UUID,
    preferred_county: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return dispatch_service.dispatch_expert_to_ticket(db, ticket_id, preferred_county)


@router.post("/auto-dispatch")
def auto_dispatch(
    county: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return dispatch_service.auto_dispatch_pending_tickets(db, county)