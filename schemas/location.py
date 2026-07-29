from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from decimal import Decimal

class LocationBase(BaseModel):
    latitude: Decimal
    longitude: Decimal
    captured_at: datetime

class LocationCreate(LocationBase):
    pass

class LocationRead(LocationBase):
    model_config = ConfigDict(from_attributes=True)
    
    location_id: UUID
    created_at: datetime

class LocationUpdate(LocationBase):
    location_id: UUID
