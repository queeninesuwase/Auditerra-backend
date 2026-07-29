from sqlalchemy import Column, String, TEXT, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
import uuid

from database import Base

class ServiceTicket(Base):
    __tablename__ = "service_ticket"

    ticket_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("farmer.farmer_id"), nullable=False)
    expert_id = Column(UUID(as_uuid=True), ForeignKey("field_expert.expert_id"), nullable=True)
    
    issue_category = Column(
        ENUM("soil", "crop", "water", "erosion", name="issue_category_enum"), 
        nullable=False
    )
    status = Column(
        ENUM("pending", "dispatched", "resolved", "closed", name="ticket_status_enum"), 
        nullable=False, 
        default="pending"
    )
    description = Column(TEXT, nullable=False)

    
    farmer = relationship("Farmer", back_populates="service_tickets")
    expert = relationship("FieldExpert", back_populates="service_tickets")
    diagnostic_log = relationship("DiagnosticLog", back_populates="service_ticket", uselist=False)
