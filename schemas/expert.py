from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class FieldExpertBase(BaseModel):
    name: str
    email: str
    phone: str
    assigned_territory: str
    expertise_area: Optional[str] = None
    location_id: Optional[UUID] = None

class FieldExpertCreate(FieldExpertBase):
    password: str  

class FieldExpertRead(FieldExpertBase):
    model_config = ConfigDict(from_attributes=True)
    
    expert_id: UUID
    last_login: Optional[datetime] = None

class FieldExpertUpdate(FieldExpertBase):
    expert_id: UUID
