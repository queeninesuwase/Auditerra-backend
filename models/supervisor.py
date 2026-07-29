from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from database import Base

class InstitutionalSupervisor(Base):
    __tablename__ = "institutional_supervisor"

    supervisor_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id = Column(UUID(as_uuid=True), ForeignKey("location.location_id"), nullable=True)
    expert_id = Column(UUID(as_uuid=True), ForeignKey("field_expert.expert_id"), nullable=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    last_login = Column(TIMESTAMP(timezone=True), nullable=True)
    institution_name = Column(String(255), nullable=False)

    
    location = relationship("Location", back_populates="supervisors")
    field_experts = relationship("FieldExpert", back_populates="supervisor")
