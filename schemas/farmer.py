from pydantic import BaseModel, ConfigDict
from uuid import UUID

class FarmerBase(BaseModel):
    name: str
    phone: str
    unique_handshake_code: str
    county_location: str
    sub_county: str
    village: str
    landmark: str
    preferred_language: str

class FarmerCreate(FarmerBase):
    pass

class FarmerRead(FarmerBase):
    model_config = ConfigDict(from_attributes=True)
    
    farmer_id: UUID

class FarmerUpdate(FarmerBase):
    farmer_id: UUID
