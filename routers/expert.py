from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from schemas.expert import FieldExpertCreate, FieldExpertRead, FieldExpertUpdate
from services import expert_service

router = APIRouter(prefix="/experts", tags=["experts"])

@router.get("/", response_model=list[FieldExpertRead])
def list_experts(db: Session = Depends(get_db)):
    return expert_service.list_experts(db)

@router.get("/{expert_id}", response_model=FieldExpertRead)
def get_expert(expert_id: UUID, db: Session = Depends(get_db)):
    return expert_service.get_expert(db, expert_id)

@router.post("/", response_model=FieldExpertRead, status_code=status.HTTP_201_CREATED)
def create_expert(data: FieldExpertCreate, db: Session = Depends(get_db)):
    return expert_service.create_expert(db, data)

@router.put("/{expert_id}", response_model=FieldExpertRead)
def update_expert(expert_id: UUID, data: FieldExpertUpdate, db: Session = Depends(get_db)):
    return expert_service.update_expert(db, expert_id, data)

@router.delete("/{expert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expert(expert_id: UUID, db: Session = Depends(get_db)):
    expert_service.delete_expert(db, expert_id)
    return None
