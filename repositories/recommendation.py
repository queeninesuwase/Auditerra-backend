from sqlalchemy.orm import Session
from uuid import UUID
from models.recommendation import AIRecommendation

class AIRecommendationRepository:
    def __init__(self):
        self.model = AIRecommendation

    def get(self, db: Session, recommendation_id: UUID):
        return db.get(AIRecommendation, recommendation_id)
    
    def get_all(self, db: Session):
        return db.query(AIRecommendation).all()

    def get_by_farmer(self, db: Session, farmer_id: UUID):
        return db.query(AIRecommendation).filter(AIRecommendation.farmer_id == farmer_id).all()

    def create(self, db: Session, data: dict):
        recommendation = AIRecommendation(**data)
        db.add(recommendation)
        db.commit()
        db.refresh(recommendation)
        return recommendation

    def update(self, db: Session, db_obj: AIRecommendation, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: AIRecommendation):
        db.delete(db_obj)
        db.commit()

recommendation_repository = AIRecommendationRepository()
