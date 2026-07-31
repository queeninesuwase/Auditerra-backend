
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from schemas.recommendation import AIRecommendationCreate, AIRecommendationRead, AIRecommendationUpdate
from services import recommendation_service

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/", response_model=list[AIRecommendationRead])
def list_recommendations(db: Session = Depends(get_db)):
    return recommendation_service.list_recommendations(db)


@router.get("/{recommendation_id}", response_model=AIRecommendationRead)
def get_recommendation(recommendation_id: UUID, db: Session = Depends(get_db)):
    return recommendation_service.get_recommendation(db, recommendation_id)


@router.get("/farmer/{farmer_id}", response_model=list[AIRecommendationRead])
def get_by_farmer(farmer_id: UUID, db: Session = Depends(get_db)):
    return recommendation_service.get_recommendations_by_farmer(db, farmer_id)


@router.get("/log/{log_id}", response_model=AIRecommendationRead)
def get_by_log(log_id: UUID, db: Session = Depends(get_db)):
    return recommendation_service.get_recommendation_by_log(db, log_id)


@router.post("/", response_model=AIRecommendationRead, status_code=status.HTTP_201_CREATED)
def create_recommendation(data: AIRecommendationCreate, db: Session = Depends(get_db)):
    return recommendation_service.create_recommendation(db, data)


@router.post("/generate")
def generate_prescription(log_id: UUID, staff_id: UUID, db: Session = Depends(get_db)):
    return recommendation_service.generate_ai_prescription(db, log_id, staff_id)


@router.put("/{recommendation_id}", response_model=AIRecommendationRead)
def update_recommendation(recommendation_id: UUID, data: AIRecommendationUpdate, db: Session = Depends(get_db)):
    return recommendation_service.update_recommendation(db, recommendation_id, data)


@router.post("/{recommendation_id}/sms-delivered")
def mark_sms_delivered(recommendation_id: UUID, db: Session = Depends(get_db)):
    return recommendation_service.mark_sms_delivered(db, recommendation_id)


@router.post("/{recommendation_id}/sms-failed")
def mark_sms_failed(recommendation_id: UUID, db: Session = Depends(get_db)):
    return recommendation_service.mark_sms_failed(db, recommendation_id)


@router.post("/{recommendation_id}/expert-notified")
def mark_expert_notified(recommendation_id: UUID, db: Session = Depends(get_db)):
    return recommendation_service.mark_expert_notified(db, recommendation_id)


@router.delete("/{recommendation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recommendation(recommendation_id: UUID, db: Session = Depends(get_db)):
    recommendation_service.delete_recommendation(db, recommendation_id)
    return None