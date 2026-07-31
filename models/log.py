
import uuid
from sqlalchemy import Column, Numeric, LargeBinary, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class DiagnosticLog(Base):
    __tablename__ = "diagnostic_log"

    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id = Column(UUID(as_uuid=True), ForeignKey("location.location_id"), nullable=False)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("service_ticket.ticket_id"), nullable=True, unique=True)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("institution_staff.staff_id"), nullable=False)
    soil_ph = Column(Numeric(3, 1), nullable=True)
    nitrogen_ppm = Column(Numeric(10, 2), nullable=True)
    phosphorous_ppm = Column(Numeric(10, 2), nullable=True)
    potassium_ppm = Column(Numeric(10, 2), nullable=True)
    soil_images = Column(LargeBinary, nullable=True)

    location = relationship("Location", back_populates="logs")
    ticket = relationship("ServiceTicket", back_populates="log")
    expert = relationship("InstitutionStaff", back_populates="logs")
    recommendation = relationship("AIRecommendation", back_populates="log", uselist=False)