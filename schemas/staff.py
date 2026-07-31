
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class StaffBase(BaseModel):
    role: str
    location_id: UUID | None = None
    name: str
    email: str
    phone: str
    institution_name: str
    assigned_county: str
    expertise_area: list[str] | None = None
    preferred_language: str | None = None


class InstitutionStaffCreate(StaffBase):
    password: str


class InstitutionStaffRead(StaffBase):
    model_config = ConfigDict(from_attributes=True)

    staff_id: UUID
    last_login: datetime | None = None


class InstitutionStaffUpdate(StaffBase):
    staff_id: UUID