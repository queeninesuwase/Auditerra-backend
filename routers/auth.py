
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from repositories.user import user_repository
from repositories.staff import staff_repository
from core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["authentication"])

_login_attempts = {}


def _is_locked(email: str):
    record = _login_attempts.get(email)
    if not record:
        return None
    if record.get("locked_until") and datetime.now(timezone.utc) < record["locked_until"]:
        return record["locked_until"]
    return None


def _record_failed_attempt(email: str):
    now = datetime.now(timezone.utc)
    record = _login_attempts.get(email, {"count": 0, "locked_until": None})
    record["count"] += 1
    if record["count"] >= 5:
        record["locked_until"] = now + timedelta(minutes=15)
        record["count"] = 0
    _login_attempts[email] = record
    return record.get("locked_until")


def _clear_attempts(email: str):
    _login_attempts.pop(email, None)


@router.post("/login", status_code=status.HTTP_200_OK)
def login_staff(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    locked_until = _is_locked(form_data.username)
    if locked_until:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Account locked. Try again after {locked_until.isoformat()}"
        )

    user = user_repository.get_by_email(db, form_data.username)
    if not user or not user.password_hash or not verify_password(form_data.password, user.password_hash):
        lock_time = _record_failed_attempt(form_data.username)
        if lock_time:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many failed attempts. Locked until {lock_time.isoformat()}"
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password parameters provided"
        )

    _clear_attempts(form_data.username)

    staff = staff_repository.get(db, user.user_id)
    if staff:
        staff_repository.update(db, staff, {"last_login": datetime.now(timezone.utc)})

    token = create_access_token(data={"sub": str(user.user_id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}