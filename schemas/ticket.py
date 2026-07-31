
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class ServiceTicketBase(BaseModel):
    farmer_id: UUID
    staff_id: UUID | None = None
    issue_category: str
    status: str
    description: str | None = None


class ServiceTicketCreate(ServiceTicketBase):
    pass


class ServiceTicketRead(ServiceTicketBase):
    model_config = ConfigDict(from_attributes=True)

    ticket_id: UUID
    created_at: datetime


class ServiceTicketUpdate(ServiceTicketBase):
    ticket_id: UUID