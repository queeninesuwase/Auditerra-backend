from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, Literal

class ServiceTicketBase(BaseModel):
    farmer_id: UUID
    issue_category: Literal["soil", "crop", "water", "erosion"]
    status: Literal["pending", "cancelled", "dispatched", "resolved"]
    description: str
    expert_id: Optional[UUID] = None

class ServiceTicketCreate(BaseModel):
    farmer_id: UUID
    issue_category: Literal["soil", "crop", "water", "erosion"]
    description: str

class ServiceTicketRead(ServiceTicketBase):
    model_config = ConfigDict(from_attributes=True)
    
    ticket_id: UUID

class ServiceTicketUpdate(ServiceTicketBase):
    ticket_id: UUID
