
import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class Farmer(Base):
    __tablename__ = "farmer"

    farmer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    unique_handshake_code = Column(String(10), nullable=False)
    county_location = Column(String(20), nullable=False)
    sub_county = Column(String(20), nullable=False)
    village = Column(String(20), nullable=False)
    landmark = Column(String(20), nullable=False)
    preferred_language = Column(String(10), nullable=False)

    service_tickets = relationship("ServiceTicket", back_populates="farmer")
    recommendations = relationship("AIRecommendation", back_populates="farmer")