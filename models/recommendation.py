import uuid
from sqlalchemy import Column, TEXT, TIMESTAMP, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship

from database import Base

class AIRecommendation(Base):
    __tablename__ = "ai_recommendation"

    recommendation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    log_id = Column(UUID(as_uuid=True), ForeignKey("diagnostic_log.log_id"), nullable=False)
    expert_id = Column(UUID(as_uuid=True), ForeignKey("institution_staff.staff_id"), nullable=False)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("farmer.farmer_id"), nullable=False)
    
    recommended_text = Column(TEXT, nullable=False)
    expert_recommendation_delivery = Column(
        ENUM("pending", "delivered", "failed", name="delivery_status_enum"), 
        nullable=False, 
        default="pending"
    )
    sms_delivery_status = Column(
        ENUM("pending", "delivered", "failed", name="sms_status_enum"), 
        nullable=False, 
        default="pending"
    )
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))

    
    diagnostic_log = relationship("DiagnosticLog", back_populates="recommendation")
    expert = relationship("InstitutionStaff", back_populates="recommendations")
    farmer = relationship("Farmer", back_populates="recommendations")
