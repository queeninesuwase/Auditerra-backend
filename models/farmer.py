
import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class Farmer(Base):
    __tablename__ = "farmer"

    farmer_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"), primary_key=True)
    unique_handshake_code = Column(String(10), nullable=False)
    sub_county = Column(String(20), nullable=False)
    village = Column(String(20), nullable=False)
    landmark = Column(String(20), nullable=False)
    

    user = relationship("User", back_populates="farmer_profile")
    service_tickets = relationship("ServiceTicket", back_populates="farmer")
    recommendations = relationship("AIRecommendation", back_populates="farmer")

    @property
    def name(self): 
        return self.user.name if self.user else None

    @property
    def email(self): 
        return self.user.email if self.user else None

    @property
    def phone(self): 
        return self.user.phone if self.user else None

    @property
    def county(self): 
        return self.user.county if self.user else None

    @property
    def county_location(self): 
        return self.user.county if self.user else None

    @property
    def preferred_language(self): 
        return self.user.preferred_language if self.user else None