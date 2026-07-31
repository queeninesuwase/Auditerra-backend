
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class AIRecommendationBase(BaseModel):
    log_id: UUID
    farmer_id: UUID
    staff_id: UUID
    recommended_text: str
    expert_recommendation_delivery: str
    sms_delivery_status: str


class AIRecommendationCreate(AIRecommendationBase):
    pass


class AIRecommendationRead(AIRecommendationBase):
    model_config = ConfigDict(from_attributes=True)

    recommendation_id: UUID
    created_at: datetime


class AIRecommendationUpdate(AIRecommendationBase):
    recommendation_id: UUID