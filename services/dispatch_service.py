
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from repositories.ticket import ticket_repository
from repositories.staff import staff_repository
from repositories.farmer import farmer_repository
from services.ticket_service import assign_expert


def dispatch_expert_to_ticket(
    db: Session,
    ticket_id: UUID,
    preferred_county: Optional[str] = None
):
    ticket = ticket_repository.get(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.status != "pending":
        raise HTTPException(status_code=409, detail="Ticket is not in pending state")
    
    farmer = farmer_repository.get(db, ticket.farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    target_county = preferred_county or farmer.county_location
    
    candidates = staff_repository.get_by_county_and_role(
        db, county=target_county, role="field_expert"
    )
    
    if not candidates:
        candidates = staff_repository.get_by_role(db, "field_expert")
    
    if not candidates:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No available field experts for dispatch"
        )
    
    best_expert = _score_candidates(db, candidates, farmer, ticket)
    
    updated_ticket = assign_expert(db, ticket_id, best_expert.staff_id)
    
    farmer_message = _build_farmer_sms(farmer, best_expert, updated_ticket)
    expert_message = _build_expert_push(farmer, best_expert, updated_ticket)
    
    return {
        "ticket_id": ticket_id,
        "expert_id": best_expert.staff_id,
        "expert_name": best_expert.name,
        "expert_phone": best_expert.phone,
        "estimated_arrival": "Within 24 hours",
        "farmer_notification": farmer_message,
        "expert_notification": expert_message
    }


def _score_candidates(db, candidates, farmer, ticket):
    scored = []
    for expert in candidates:
        score = 0
        
        if expert.assigned_county == farmer.county_location:
            score += 40
        
        expert_lang = getattr(expert, "preferred_language", None)
        farmer_lang = getattr(farmer, "preferred_language", None)
        if expert_lang and farmer_lang and expert_lang == farmer_lang:
            score += 25
        
        expertise_areas = getattr(expert, "expertise_area", []) or []
        if ticket.issue_category in expertise_areas:
            score += 35
        
        scored.append((score, expert))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


def _build_farmer_sms(farmer, expert, ticket):
    return (
        f"Hello {farmer.name}, your reported issue ({ticket.issue_category}) "
        f"has been assigned to {expert.name}. "
        f"Estimated arrival: Within 24 hours. "
        f"Your security code: {farmer.unique_handshake_code}. "
        f"Do not share this code until the expert arrives."
    )


def _build_expert_push(farmer, expert, ticket):
    return {
        "ticket_id": str(ticket.ticket_id),
        "farmer_name": farmer.name,
        "farmer_phone": farmer.phone,
        "county": farmer.county_location,
        "sub_county": getattr(farmer, "sub_county", ""),
        "village": getattr(farmer, "village", ""),
        "landmark": getattr(farmer, "landmark", ""),
        "issue_category": ticket.issue_category,
        "issue_description": getattr(ticket, "description", ""),
        "handshake_code": farmer.unique_handshake_code
    }


def auto_dispatch_pending_tickets(db: Session, county: Optional[str] = None):
    pending = ticket_repository.get_by_status(db, "pending")
    results = []
    for ticket in pending:
        farmer = farmer_repository.get(db, ticket.farmer_id)
        if county and farmer.county_location != county:
            continue
        try:
            result = dispatch_expert_to_ticket(db, ticket.ticket_id)
            results.append({
                "ticket_id": ticket.ticket_id,
                "status": "dispatched",
                "expert_id": result["expert_id"]
            })
        except HTTPException:
            results.append({
                "ticket_id": ticket.ticket_id,
                "status": "failed",
                "reason": "No suitable expert found"
            })
    return results