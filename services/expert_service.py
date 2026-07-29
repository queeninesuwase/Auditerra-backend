from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

from repositories.expert import expert_repository
from schemas.expert import FieldExpertCreate, FieldExpertUpdate

def get_expert(db: Session, expert_id: UUID):
    expert = expert_repository.get(db, expert_id)
    if not expert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Field expert not found"
        )
    return expert

def list_experts(db: Session):
    return expert_repository.get_all(db)

def create_expert(db: Session, data: FieldExpertCreate):
    
    existing = expert_repository.get_by_email(db, data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An expert with this email is already registered"
        )
    
    
    payload = data.model_dump()
    raw_password = payload.pop("password")
    
    
    payload["password_hash"] = f"hashed_{raw_password}"
    
    return expert_repository.create(db, payload)

def update_expert(db: Session, expert_id: UUID, data: FieldExpertUpdate):
    expert = get_expert(db, expert_id)
    return expert_repository.update(db, expert, data.model_dump(exclude_unset=True))

def delete_expert(db: Session, expert_id: UUID):
    expert = get_expert(db, expert_id)
    expert_repository.delete(db, expert)
