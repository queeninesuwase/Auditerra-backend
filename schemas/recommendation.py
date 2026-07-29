from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Literal

class AIRecommendationBase(BaseModel):
    log_id: UUID
    expert_id: UUID
    farmer_id: UUID
    recommended_text: str
    expert_recommendation_delivery: Literal["pending", "delivered", "failed"]
    sms_delivery_status: Literal["pending", "delivered", "failed"]

class AIRecommendationCreate(BaseModel):
    log_id: UUID
    expert_id: UUID
    farmer_id: UUID
    recommended_text: str

class AIRecommendationRead(AIRecommendationBase):
    model_config = ConfigDict(from_attributes=True)
    
    recommendation_id: UUID
    created_at: datetime

class AIRecommendationUpdate(AIRecommendationBase):
    recommendation_id: UUID
