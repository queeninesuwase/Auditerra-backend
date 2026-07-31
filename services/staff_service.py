
import os
import hmac
import hashlib
import base64
import struct
import time
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from core.security import hash_password, verify_password
from repositories.staff import staff_repository
from repositories.farmer import farmer_repository
from repositories.ticket import ticket_repository
from repositories.log import log_repository
from repositories.recommendation import recommendation_repository
from schemas.staff import InstitutionStaffCreate, InstitutionStaffUpdate


def get_staff(db: Session, staff_id: UUID):
    staff = staff_repository.get(db, staff_id)
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution staff member profile not found"
        )
    return staff


def list_staff(db: Session):
    return staff_repository.get_all(db)


def get_field_experts(db: Session):
    return staff_repository.get_by_role(db, "field_expert")


def get_supervisors(db: Session):
    return staff_repository.get_by_role(db, "institutional_supervisor")


def get_experts_by_county(db: Session, county: str):
    return staff_repository.get_by_county_and_role(db, county, "field_expert")


def create_staff(db: Session, data: InstitutionStaffCreate):
    existing = staff_repository.get_by_email(db, data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A staff member with this email is already registered"
        )
    payload = data.model_dump()
    raw_password = payload.pop("password")
    payload["password_hash"] = hash_password(raw_password)
    if payload.get("role") not in ("institutional_supervisor", "field_expert"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be 'institutional_supervisor' or 'field_expert'"
        )
    return staff_repository.create(db, payload)


def update_staff(db: Session, staff_id: UUID, data: InstitutionStaffUpdate):
    staff = get_staff(db, staff_id)
    payload = data.model_dump(exclude_unset=True)
    if "role" in payload and payload["role"] not in ("institutional_supervisor", "field_expert"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role value"
        )
    return staff_repository.update(db, staff, payload)


def delete_staff(db: Session, staff_id: UUID):
    staff = get_staff(db, staff_id)
    staff_repository.delete(db, staff)


def authenticate_staff(db: Session, email: str, password: str):
    staff = staff_repository.get_by_email(db, email)
    if not staff or not verify_password(password, staff.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    staff_repository.update(db, staff, {"last_login": datetime.now(timezone.utc)})
    return staff


def require_supervisor(db: Session, staff_id: UUID):
    staff = get_staff(db, staff_id)
    if staff.role != "institutional_supervisor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This operation requires institutional supervisor privileges"
        )
    return staff


def require_field_expert(db: Session, staff_id: UUID):
    staff = get_staff(db, staff_id)
    if staff.role != "field_expert":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This operation requires a certified field expert"
        )
    return staff


def generate_totp_secret() -> str:
    return base64.b32encode(os.urandom(20)).decode("utf-8")


def verify_totp(secret: str, code: str, window: int = 1) -> bool:
    key = base64.b32decode(secret.upper())
    current_time = int(time.time()) // 30
    for offset in range(-window, window + 1):
        target_time = struct.pack(">Q", current_time + offset)
        h = hmac.new(key, target_time, hashlib.sha1).digest()
        offset_byte = h[-1] & 0x0f
        code_int = (struct.unpack(">I", h[offset_byte:offset_byte + 4])[0] & 0x7fffffff) % 1000000
        if f"{code_int:06d}" == code:
            return True
    return False


def verify_expert_totp(db: Session, supervisor_id: UUID, expert_id: UUID, totp_code: str):
    require_supervisor(db, supervisor_id)
    expert = require_field_expert(db, expert_id)
    if not getattr(expert, "totp_secret", None):
        raise HTTPException(status_code=400, detail="Expert has no TOTP configured")
    if not verify_totp(expert.totp_secret, totp_code):
        raise HTTPException(status_code=403, detail="Invalid TOTP code")
    return {"verified": True, "expert_id": expert_id}


def get_dashboard_metrics(db: Session, supervisor_id: UUID):
    require_supervisor(db, supervisor_id)

    total_farmers = len(farmer_repository.get_all(db))
    total_experts = len(staff_repository.get_by_role(db, "field_expert"))
    total_tickets = len(ticket_repository.get_all(db))

    pending = len(ticket_repository.get_by_status(db, "pending"))
    dispatched = len(ticket_repository.get_by_status(db, "dispatched"))
    resolved = len(ticket_repository.get_by_status(db, "resolved"))
    cancelled = len(ticket_repository.get_by_status(db, "cancelled"))

    total_logs = len(log_repository.get_all(db))
    total_recommendations = len(recommendation_repository.get_all(db))

    return {
        "total_farmers": total_farmers,
        "total_field_experts": total_experts,
        "total_tickets": total_tickets,
        "tickets_by_status": {
            "pending": pending,
            "dispatched": dispatched,
            "resolved": resolved,
            "cancelled": cancelled
        },
        "total_diagnostics": total_logs,
        "total_ai_recommendations": total_recommendations
    }


def search_expert_by_farmer(db: Session, supervisor_id: UUID, farmer_id: UUID):
    require_supervisor(db, supervisor_id)
    farmer = farmer_repository.get(db, farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    tickets = ticket_repository.get_by_farmer(db, farmer_id)
    active_ticket = None
    for t in tickets:
        if t.status in ("pending", "dispatched"):
            active_ticket = t
            break

    if not active_ticket or not active_ticket.staff_id:
        return {"farmer_id": farmer_id, "expert": None}

    expert = staff_repository.get(db, active_ticket.staff_id)
    return {
        "farmer_id": farmer_id,
        "farmer_name": farmer.name,
        "ticket_id": active_ticket.ticket_id,
        "ticket_status": active_ticket.status,
        "expert": {
            "staff_id": expert.staff_id,
            "name": expert.name,
            "phone": expert.phone,
            "email": expert.email,
            "assigned_county": expert.assigned_county
        } if expert else None
    }


def list_farmers_with_open_issues(db: Session, supervisor_id: UUID):
    require_supervisor(db, supervisor_id)
    farmers = farmer_repository.get_all(db)
    result = []
    for farmer in farmers:
        tickets = ticket_repository.get_by_farmer(db, farmer.farmer_id)
        open_tickets = [t for t in tickets if t.status in ("pending", "dispatched")]
        if open_tickets:
            result.append({
                "farmer_id": farmer.farmer_id,
                "name": farmer.name,
                "phone": farmer.phone,
                "county": farmer.county_location,
                "open_issues": len(open_tickets),
                "latest_issue": open_tickets[-1].issue_category if open_tickets else None
            })
    return result


def generate_impact_report(db: Session, supervisor_id: UUID, county: str = None):
    require_supervisor(db, supervisor_id)

    farmers = farmer_repository.get_all(db)
    tickets = ticket_repository.get_all(db)
    logs = log_repository.get_all(db)
    recommendations = recommendation_repository.get_all(db)

    if county:
        farmers = [f for f in farmers if f.county_location == county]
        farmer_ids = {f.farmer_id for f in farmers}
        tickets = [t for t in tickets if t.farmer_id in farmer_ids]

    ticket_ids = {t.ticket_id for t in tickets}
    logs = [l for l in logs if l.ticket_id in ticket_ids]
    log_ids = {l.log_id for l in logs}
    recommendations = [r for r in recommendations if r.log_id in log_ids]

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "county_filter": county,
        "summary": {
            "farmers_served": len(farmers),
            "tickets_raised": len(tickets),
            "diagnostics_completed": len(logs),
            "recommendations_issued": len(recommendations)
        },
        "soil_health_summary": _aggregate_soil_metrics(logs),
        "delivery_summary": {
            "sms_pending": len([r for r in recommendations if r.sms_delivery_status == "pending"]),
            "sms_delivered": len([r for r in recommendations if r.sms_delivery_status == "delivered"]),
            "sms_failed": len([r for r in recommendations if r.sms_delivery_status == "failed"])
        },
        "records": [
            {
                "farmer_name": f.name,
                "county": f.county_location,
                "issue": next((t.issue_category for t in tickets if t.farmer_id == f.farmer_id), None),
                "expert_assigned": next((t.staff_id for t in tickets if t.farmer_id == f.farmer_id and t.staff_id), None)
            }
            for f in farmers
        ]
    }
    return report


def _aggregate_soil_metrics(logs):
    if not logs:
        return {}
    ph_values = [l.soil_ph for l in logs if getattr(l, "soil_ph", None) is not None]
    nitrogen = [l.nitrogen_ppm for l in logs if getattr(l, "nitrogen_ppm", None) is not None]
    phosphorus = [l.phosphorous_ppm for l in logs if getattr(l, "phosphorous_ppm", None) is not None]
    potassium = [l.potassium_ppm for l in logs if getattr(l, "potassium_ppm", None) is not None]

    def avg(lst):
        return sum(lst) / len(lst) if lst else None

    return {
        "avg_soil_ph": avg(ph_values),
        "avg_nitrogen_ppm": avg(nitrogen),
        "avg_phosphorus_ppm": avg(phosphorus),
        "avg_potassium_ppm": avg(potassium),
        "samples_collected": len(logs)
    }