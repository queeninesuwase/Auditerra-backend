import uuid
import enum
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from database import Base


class UserRole(str, enum.Enum):
   farmer = "farmer"
   field_expert = "field_expert"
   institutional_supervisor = "institutional_supervisor"


class User(Base):
   __tablename__ = "user"


   user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   name = Column(String(255), nullable=False)
   phone = Column(String(20), unique=True, nullable=False)
   email = Column(String(255), unique=True, nullable=True)
   password_hash = Column(String(255), nullable=True)
   county = Column(String(255), nullable=False)
   preferred_language = Column(String(10), nullable=True)
  
   role = Column(
       Enum(UserRole, name="user_role"),
       nullable=False
   )
  
   created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))


   farmer_profile = relationship("Farmer", back_populates="user", uselist=False)
   staff_profile = relationship("InstitutionStaff", back_populates="user", uselist=False)



