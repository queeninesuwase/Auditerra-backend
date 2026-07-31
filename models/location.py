import uuid
from sqlalchemy import Column, Numeric, String, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base

class Location(Base):
    __tablename__ = "location"

    location_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    captured_at = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
    county = Column(String(255), nullable=False)
    country_code = Column(String(2), nullable=True)
    region_name = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)

    
    staff_members = relationship("InstitutionStaff", back_populates="location")
    diagnostic_logs = relationship("DiagnosticLog", back_populates="location")
