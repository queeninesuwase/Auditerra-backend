
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from schemas.staff import InstitutionStaffCreate, InstitutionStaffRead, InstitutionStaffUpdate
from services import staff_service

router = APIRouter(prefix="/staff", tags=["staff"])


@router.get("/", response_model=list[InstitutionStaffRead])
def list_staff(db: Session = Depends(get_db)):
    return staff_service.list_staff(db)


@router.get("/field-experts", response_model=list[InstitutionStaffRead])
def list_field_experts(db: Session = Depends(get_db)):
    return staff_service.get_field_experts(db)


@router.get("/supervisors", response_model=list[InstitutionStaffRead])
def list_supervisors(db: Session = Depends(get_db)):
    return staff_service.get_supervisors(db)


@router.get("/{staff_id}", response_model=InstitutionStaffRead)
def get_staff(staff_id: UUID, db: Session = Depends(get_db)):
    return staff_service.get_staff(db, staff_id)


@router.post("/", response_model=InstitutionStaffRead, status_code=status.HTTP_201_CREATED)
def create_staff(data: InstitutionStaffCreate, db: Session = Depends(get_db)):
    return staff_service.create_staff(db, data)


@router.put("/{staff_id}", response_model=InstitutionStaffRead)
def update_staff(staff_id: UUID, data: InstitutionStaffUpdate, db: Session = Depends(get_db)):
    return staff_service.update_staff(db, staff_id, data)


@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_staff(staff_id: UUID, db: Session = Depends(get_db)):
    staff_service.delete_staff(db, staff_id)
    return None


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    return staff_service.authenticate_staff(db, email, password)


@router.get("/{supervisor_id}/dashboard-metrics")
def dashboard_metrics(supervisor_id: UUID, db: Session = Depends(get_db)):
    return staff_service.get_dashboard_metrics(db, supervisor_id)


@router.get("/search-expert-by-farmer")
def search_expert_by_farmer(supervisor_id: UUID, farmer_id: UUID, db: Session = Depends(get_db)):
    return staff_service.search_expert_by_farmer(db, supervisor_id, farmer_id)


@router.get("/{supervisor_id}/farmers-with-open-issues")
def farmers_with_open_issues(supervisor_id: UUID, db: Session = Depends(get_db)):
    return staff_service.list_farmers_with_open_issues(db, supervisor_id)


@router.get("/{supervisor_id}/impact-report")
def impact_report(supervisor_id: UUID, county: str = None, db: Session = Depends(get_db)):
    return staff_service.generate_impact_report(db, supervisor_id, county)


@router.post("/{supervisor_id}/verify-expert-totp")
def verify_expert_totp(supervisor_id: UUID, expert_id: UUID, totp_code: str, db: Session = Depends(get_db)):
    return staff_service.verify_expert_totp(db, supervisor_id, expert_id, totp_code)