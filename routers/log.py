from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from routers.deps import get_current_user

from database import get_db
from schemas.log import DiagnosticLogCreate, DiagnosticLogRead, DiagnosticLogUpdate
from services import log_service

router = APIRouter(prefix="/logs", tags=["logs"])

@router.get("/", response_model=list[DiagnosticLogRead])
def list_logs(db: Session = Depends(get_db)):
    return log_service.list_logs(db)

@router.get("/{log_id}", response_model=DiagnosticLogRead)
def get_log(log_id: UUID, db: Session = Depends(get_db)):
    return log_service.get_log(db, log_id)

@router.post("/", response_model=DiagnosticLogRead, status_code=status.HTTP_201_CREATED)
def create_log(
    data: DiagnosticLogCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) 
):
    return log_service.create_log(db, data)

@router.put("/{log_id}", response_model=DiagnosticLogRead)
def update_log(log_id: UUID, data: DiagnosticLogUpdate, db: Session = Depends(get_db)):
    return log_service.update_log(db, log_id, data)

@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_log(log_id: UUID, db: Session = Depends(get_db)):
    log_service.delete_log(db, log_id)
    return None
