
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class Location(Base):
    __tablename__ = "location"

    location_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    captured_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))
    county = Column(String(255), nullable=False)
    country_code = Column(String(2), nullable=True)
    region_name = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("institution_staff.staff_id"), nullable=True)

    expert = relationship("InstitutionStaff", back_populates="locations")
    logs = relationship("DiagnosticLog", back_populates="location")