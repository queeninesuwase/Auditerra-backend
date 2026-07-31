from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, Literal

class InstitutionStaffBase(BaseModel):
    role: Literal["institutional_supervisor", "field_expert"]
    name: str
    email: str
    phone: str
    institution_name: str
    assigned_county: str
    expertise_area: Optional[list[str]] = None
    location_id: Optional[UUID] = None

class InstitutionStaffCreate(InstitutionStaffBase):
    password: str 

class InstitutionStaffRead(InstitutionStaffBase):
    model_config = ConfigDict(from_attributes=True)
    
    staff_id: UUID
    last_login: Optional[datetime] = None

class InstitutionStaffUpdate(InstitutionStaffBase):
    staff_id: UUID
