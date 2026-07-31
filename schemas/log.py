
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class DiagnosticLogBase(BaseModel):
    location_id: UUID
    ticket_id: UUID | None = None
    staff_id: UUID
    soil_ph: float | None = None
    nitrogen_ppm: float | None = None
    phosphorous_ppm: float | None = None
    potassium_ppm: float | None = None
    soil_images: bytes | None = None


class DiagnosticLogCreate(DiagnosticLogBase):
    pass


class DiagnosticLogRead(DiagnosticLogBase):
    model_config = ConfigDict(from_attributes=True)

    log_id: UUID


class DiagnosticLogUpdate(DiagnosticLogBase):
    log_id: UUID