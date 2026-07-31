
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class LocationBase(BaseModel):
    latitude: float
    longitude: float
    captured_at: datetime
    county: str
    country_code: str | None = None
    region_name: str | None = None
    postal_code: str | None = None
    staff_id: UUID | None = None


class LocationCreate(LocationBase):
    pass


class LocationRead(LocationBase):
    model_config = ConfigDict(from_attributes=True)

    location_id: UUID
    created_at: datetime


class LocationUpdate(LocationBase):
    location_id: UUID