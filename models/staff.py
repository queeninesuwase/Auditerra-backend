import uuid
import enum
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Enum, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base

class StaffRole(str, enum.Enum):
    institutional_supervisor = "institutional_supervisor"
    field_expert = "field_expert"

class InstitutionStaff(Base):
    __tablename__ = "institution_staff"

    staff_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(Enum(StaffRole, name="staff_role_enum"), nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey("location.location_id"), nullable=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    institution_name = Column(String(255), nullable=False)
    assigned_county = Column(String(255), nullable=False)
    expertise_area = Column(ARRAY(String(100)), nullable=True)
    last_login = Column(TIMESTAMP(timezone=True), nullable=True)

    
    location = relationship("Location", back_populates="staff_members")
    service_tickets = relationship("ServiceTicket", back_populates="expert")
    diagnostic_logs = relationship("DiagnosticLog", back_populates="expert")
    recommendations = relationship("AIRecommendation", back_populates="expert")
