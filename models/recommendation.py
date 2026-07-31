
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class AIRecommendation(Base):
    __tablename__ = "ai_recommendation"

    recommendation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    log_id = Column(UUID(as_uuid=True), ForeignKey("diagnostic_log.log_id"), nullable=False)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("farmer.farmer_id"), nullable=False)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("institution_staff.staff_id"), nullable=False)
    recommended_text = Column(Text, nullable=False)
    expert_recommendation_delivery = Column(
        Enum("pending", "delivered", "failed", name="expert_delivery_status"),
        nullable=False,
        default="pending"
    )
    sms_delivery_status = Column(
        Enum("pending", "delivered", "failed", name="sms_delivery_status"),
        nullable=False,
        default="pending"
    )
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))

    log = relationship("DiagnosticLog", back_populates="recommendation")
    farmer = relationship("Farmer", back_populates="recommendations")
    expert = relationship("InstitutionStaff", back_populates="recommendations")