from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from repositories.staff import staff_repository
from core.security import verify_password, create_access_token, SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/auth", tags=["authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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

    staff = staff_repository.get_by_email(db, form_data.username)

    if not staff or not verify_password(form_data.password, staff.password_hash):
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
    staff_repository.update(db, staff, {"last_login": datetime.now(timezone.utc)})

    token_data = {"sub": str(staff.staff_id), "role": staff.role.value}
    token = create_access_token(data=token_data)

    return {"access_token": token, "token_type": "bearer"}


async def get_current_staff(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        staff_id: str = payload.get("sub")
        if staff_id is None:
            raise credentials_exception
    except jwt.PyJWTError: 
        raise credentials_exception

    staff = staff_repository.get(db, staff_id)
    if staff is None:
        raise credentials_exception
    return staff


def require_role(role: str):
    def role_checker(current_staff = Depends(get_current_staff)):
        if current_staff.role.value != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires {role} privileges"
            )
        return current_staff
    return role_checker


require_supervisor = require_role("institutional_supervisor")
require_field_expert = require_role("field_expert")
