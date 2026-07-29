from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from database import Base

class FieldExpert(Base):
    __tablename__ = "field_expert"

    expert_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id = Column(UUID(as_uuid=True), ForeignKey("location.location_id"), nullable=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    assigned_territory = Column(String(255), nullable=False)
    expertise_area = Column(String(100), nullable=True)
    last_login = Column(TIMESTAMP(timezone=True), nullable=True)


    location = relationship("Location", back_populates="field_experts")
    supervisor = relationship("InstitutionalSupervisor", back_populates="field_experts")
    service_tickets = relationship("ServiceTicket", back_populates="expert")
    diagnostic_logs = relationship("DiagnosticLog", back_populates="expert")
    recommendations = relationship("AIRecommendation", back_populates="expert")
