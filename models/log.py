from sqlalchemy import Column, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from database import Base

class DiagnosticLog(Base):
    __tablename__ = "diagnostic_log"

    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id = Column(UUID(as_uuid=True), ForeignKey("location.location_id"), nullable=False)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("service_ticket.ticket_id"), unique=True, nullable=True)
    expert_id = Column(UUID(as_uuid=True), ForeignKey("field_expert.expert_id"), nullable=False)
    
    nitrogen_ppm = Column(Numeric(10, 2), nullable=True)
    phosphorus_ppm = Column(Numeric(10, 2), nullable=True)
    soil_ph = Column(Numeric(3, 1), nullable=True)

    
    location = relationship("Location", back_populates="diagnostic_logs")
    service_ticket = relationship("ServiceTicket", back_populates="diagnostic_log")
    expert = relationship("FieldExpert", back_populates="diagnostic_logs")
    recommendation = relationship("AIRecommendation", back_populates="diagnostic_log", uselist=False)
