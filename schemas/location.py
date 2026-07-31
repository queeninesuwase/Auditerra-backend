from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional

class LocationBase(BaseModel):
    latitude: Decimal
    longitude: Decimal
    captured_at: datetime
    county: str
    country_code: Optional[str] = None
    region_name: Optional[str] = None
    postal_code: Optional[str] = None

class LocationCreate(LocationBase):
    pass

class LocationRead(LocationBase):
    model_config = ConfigDict(from_attributes=True)
    
    location_id: UUID
    created_at: datetime

class LocationUpdate(LocationBase):
    location_id: UUID
