
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, ARRAY, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class InstitutionStaff(Base):
    __tablename__ = "institution_staff"

    staff_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), primary_key=True)
    institution_name = Column(String(255), nullable=False)
    expertise_area = Column(ARRAY(String(100)), nullable=True)
    location_id = Column(UUID(as_uuid=True), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    totp_secret = Column(String(255), nullable=True)

    user = relationship("User", back_populates="staff_profile")
    tickets = relationship("ServiceTicket", back_populates="expert")
    logs = relationship("DiagnosticLog", back_populates="expert")
    recommendations = relationship("AIRecommendation", back_populates="expert")
    locations = relationship("Location", back_populates="expert")


@property
def name(self): return self.user.name if self.user else None
@property
def email(self): return self.user.email if self.user else None
@property
def phone(self): return self.user.phone if self.user else None
@property
def county(self): return self.user.county if self.user else None
@property
def assigned_county(self): return self.user.county if self.user else None
@property
def preferred_language(self): return self.user.preferred_language if self.user else None
@property
def role(self): return self.user.role if self.user else None