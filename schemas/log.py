from pydantic import BaseModel, ConfigDict
from uuid import UUID
from decimal import Decimal
from typing import Optional

class DiagnosticLogBase(BaseModel):
    location_id: UUID
    expert_id: UUID
    ticket_id: Optional[UUID] = None
    nitrogen_ppm: Optional[Decimal] = None
    phosphorus_ppm: Optional[Decimal] = None
    potassium_ppm: Optional[Decimal] = None
    soil_ph: Optional[Decimal] = None

class DiagnosticLogCreate(DiagnosticLogBase):
    pass

class DiagnosticLogRead(DiagnosticLogBase):
    model_config = ConfigDict(from_attributes=True)
    
    log_id: UUID
   
class DiagnosticLogUpdate(DiagnosticLogBase):
    log_id: UUID
