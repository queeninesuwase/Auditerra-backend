
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class UserBase(BaseModel):
    name: str
    phone: str
    email: str | None = None
    county: str
    preferred_language: str | None = None
    role: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    created_at: datetime