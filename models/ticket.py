
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class ServiceTicket(Base):
    __tablename__ = "service_ticket"

    ticket_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("farmer.farmer_id"), nullable=False)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("institution_staff.staff_id"), nullable=True)
    issue_category = Column(
        Enum("soil", "crop", "water", "erosion", name="issue_category"),
        nullable=False
    )
    status = Column(
        Enum("pending", "dispatched", "resolved", "cancelled", name="ticket_status"),
        nullable=False,
        default="pending"
    )
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))

    farmer = relationship("Farmer", back_populates="service_tickets")
    expert = relationship("InstitutionStaff", back_populates="tickets")
    log = relationship("DiagnosticLog", back_populates="ticket", uselist=False)