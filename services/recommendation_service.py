from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

from repositories.recommendation import recommendation_repository
from schemas.recommendation import AIRecommendationCreate, AIRecommendationUpdate

def get_recommendation(db: Session, recommendation_id: UUID):
    rec = recommendation_repository.get(db, recommendation_id)
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="AI prescription summary entry not found"
        )
    return rec

def list_recommendations(db: Session):
    return recommendation_repository.get_all(db)

def create_recommendation(db: Session, data: AIRecommendationCreate):
    payload = data.model_dump()
    payload["expert_recommendation_delivery"] = "pending"
    payload["sms_delivery_status"] = "pending"
    
    
    return recommendation_repository.create(db, payload)

def update_recommendation(db: Session, recommendation_id: UUID, data: AIRecommendationUpdate):
    rec = get_recommendation(db, recommendation_id)
    return recommendation_repository.update(db, rec, data.model_dump(exclude_unset=True))

def delete_recommendation(db: Session, recommendation_id: UUID):
    rec = get_recommendation(db, recommendation_id)
    recommendation_repository.delete(db, rec)
