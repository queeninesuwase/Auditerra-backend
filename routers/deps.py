
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from uuid import UUID

from core.security import SECRET_KEY, ALGORITHM
from database import get_db
from repositories.staff import staff_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        staff_id: str = payload.get("sub")
        role: str = payload.get("role")
        if staff_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token properties"
            )
        return {"staff_id": UUID(staff_id), "role": role}
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token signature has expired or is invalid"
        )


def get_current_staff(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    staff = staff_repository.get(db, current_user["staff_id"])
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Staff not found"
        )
    return staff


def require_role(role: str):
    def checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires {role} privileges"
            )
        return current_user
    return checker


require_supervisor = require_role("institutional_supervisor")
require_field_expert = require_role("field_expert")