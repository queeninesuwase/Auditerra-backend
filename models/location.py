from sqlalchemy import Column, Numeric, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from database import Base

class Location(Base):
    __tablename__ = "location"

    location_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    captured_at = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))

    
    field_experts = relationship("FieldExpert", back_populates="location")
    supervisors = relationship("InstitutionalSupervisor", back_populates="location")
    diagnostic_logs = relationship("DiagnosticLog", back_populates="location")
