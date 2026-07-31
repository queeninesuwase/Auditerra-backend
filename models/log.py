import uuid
from sqlalchemy import Column, Numeric, ForeignKey, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base

class DiagnosticLog(Base):
    __tablename__ = "diagnostic_log"

    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id = Column(UUID(as_uuid=True), ForeignKey("location.location_id"), nullable=False)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("service_ticket.ticket_id"), unique=True, nullable=True)
    expert_id = Column(UUID(as_uuid=True), ForeignKey("institution_staff.staff_id"), nullable=False)
    
    nitrogen_ppm = Column(Numeric(10, 2), nullable=True)
    phosphorus_ppm = Column(Numeric(10, 2), nullable=True)
    potassium_ppm = Column(Numeric(10, 2), nullable=True)  # New database addition
    soil_ph = Column(Numeric(3, 1), nullable=True)
    soil_images = Column(LargeBinary, nullable=True)        # BLOB database mapping

    
    location = relationship("Location", back_populates="diagnostic_logs")
    service_ticket = relationship("ServiceTicket", back_populates="diagnostic_log")
    expert = relationship("InstitutionStaff", back_populates="diagnostic_logs")
    recommendation = relationship("AIRecommendation", back_populates="diagnostic_log", uselist=False)
