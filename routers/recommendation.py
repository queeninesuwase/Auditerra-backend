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

@router.post("/", response_model=AIRecommendationRead, status_code=status.HTTP_201_CREATED)
def create_recommendation(data: AIRecommendationCreate, db: Session = Depends(get_db)):
    return recommendation_service.create_recommendation(db, data)

@router.put("/{recommendation_id}", response_model=AIRecommendationRead)
def update_recommendation(recommendation_id: UUID, data: AIRecommendationUpdate, db: Session = Depends(get_db)):
    return recommendation_service.update_recommendation(db, recommendation_id, data)

@router.delete("/{recommendation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recommendation(recommendation_id: UUID, db: Session = Depends(get_db)):
    recommendation_service.delete_recommendation(db, recommendation_id)
    return None
