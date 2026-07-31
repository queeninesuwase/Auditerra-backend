
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from repositories.recommendation import recommendation_repository
from repositories.log import log_repository
from repositories.farmer import farmer_repository
from repositories.staff import staff_repository
from repositories.ticket import ticket_repository
from schemas.recommendation import AIRecommendationCreate, AIRecommendationUpdate


def get_recommendation(db: Session, recommendation_id: UUID):
    rec = recommendation_repository.get(db, recommendation_id)
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI prescription recommendation summary entry not found"
        )
    return rec


def list_recommendations(db: Session):
    return recommendation_repository.get_all(db)


def get_recommendations_by_farmer(db: Session, farmer_id: UUID):
    return recommendation_repository.get_by_farmer(db, farmer_id)


def get_recommendation_by_log(db: Session, log_id: UUID):
    rec = recommendation_repository.get_by_log(db, log_id)
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No AI recommendation found for this diagnostic log"
        )
    return rec


def create_recommendation(db: Session, data: AIRecommendationCreate):
    log = log_repository.get(db, data.log_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent diagnostic log not found"
        )
    farmer = farmer_repository.get(db, data.farmer_id)
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target farmer not found"
        )
    staff = staff_repository.get(db, data.staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Referring expert not found"
        )
    existing = recommendation_repository.get_by_log(db, data.log_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A recommendation already exists for this diagnostic log"
        )
    payload = data.model_dump()
    payload["expert_recommendation_delivery"] = "pending"
    payload["sms_delivery_status"] = "pending"
    payload["created_at"] = datetime.now(timezone.utc)
    return recommendation_repository.create(db, payload)


def update_recommendation(db: Session, recommendation_id: UUID, data: AIRecommendationUpdate):
    rec = get_recommendation(db, recommendation_id)
    return recommendation_repository.update(db, rec, data.model_dump(exclude_unset=True))


def delete_recommendation(db: Session, recommendation_id: UUID):
    rec = get_recommendation(db, recommendation_id)
    recommendation_repository.delete(db, rec)


def mark_sms_delivered(db: Session, recommendation_id: UUID):
    rec = get_recommendation(db, recommendation_id)
    return recommendation_repository.update(db, rec, {"sms_delivery_status": "delivered"})


def mark_sms_failed(db: Session, recommendation_id: UUID):
    rec = get_recommendation(db, recommendation_id)
    return recommendation_repository.update(db, rec, {"sms_delivery_status": "failed"})


def mark_expert_notified(db: Session, recommendation_id: UUID):
    rec = get_recommendation(db, recommendation_id)
    return recommendation_repository.update(db, rec, {"expert_recommendation_delivery": "delivered"})


def mark_expert_notification_failed(db: Session, recommendation_id: UUID):
    rec = get_recommendation(db, recommendation_id)
    return recommendation_repository.update(db, rec, {"expert_recommendation_delivery": "failed"})


def generate_ai_prescription(db: Session, log_id: UUID, staff_id: UUID):
    log = log_repository.get(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Diagnostic log not found")
    staff = staff_repository.get(db, staff_id)
    if not staff or staff.role != "field_expert":
        raise HTTPException(status_code=403, detail="Only field experts can trigger AI prescriptions")

    ticket = ticket_repository.get(db, log.ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Linked ticket not found")
    farmer = farmer_repository.get(db, ticket.farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    existing = recommendation_repository.get_by_log(db, log_id)
    if existing:
        raise HTTPException(status_code=409, detail="Recommendation already generated for this log")

    recommendation_text = _call_ai_engine(log)

    rec_data = AIRecommendationCreate(
        log_id=log_id,
        farmer_id=farmer.farmer_id,
        staff_id=staff_id,
        recommended_text=recommendation_text
    )

    return create_recommendation(db, rec_data)


def _call_ai_engine(log):
    soil_ph = getattr(log, "soil_ph", None)
    nitrogen = getattr(log, "nitrogen_ppm", None)
    phosphorus = getattr(log, "phosphorous_ppm", None)
    potassium = getattr(log, "potassium_ppm", None)

    parts = []
    if soil_ph is not None:
        if soil_ph < 6.0:
            parts.append(f"Soil pH {soil_ph} is acidic. Apply agricultural lime at 2-4 tonnes/ha.")
        elif soil_ph > 7.5:
            parts.append(f"Soil pH {soil_ph} is alkaline. Apply elemental sulfur or organic matter.")
        else:
            parts.append(f"Soil pH {soil_ph} is optimal.")
    if nitrogen is not None and nitrogen < 20:
        parts.append("Nitrogen is low. Apply NPK 23:23:0 or organic manure.")
    if phosphorus is not None and phosphorus < 15:
        parts.append("Phosphorus is deficient. Apply DAP or TSP fertilizer.")
    if potassium is not None and potassium < 150:
        parts.append("Potassium is low. Apply MOP fertilizer.")

    if not parts:
        return "Soil parameters appear within normal ranges. Maintain current practices and monitor."

    return " ".join(parts)