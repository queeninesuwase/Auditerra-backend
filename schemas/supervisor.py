from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class InstitutionalSupervisorBase(BaseModel):
    name: str
    email: str
    institution_name: str
    location_id: Optional[UUID] = None
    expert_id: Optional[UUID] = None

class InstitutionalSupervisorCreate(InstitutionalSupervisorBase):
    password: str

class InstitutionalSupervisorRead(InstitutionalSupervisorBase):
    model_config = ConfigDict(from_attributes=True)
    
    supervisor_id: UUID
    last_login: Optional[datetime] = None

class InstitutionalSupervisorUpdate(InstitutionalSupervisorBase):
    supervisor_id: UUID
