from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from repositories.staff import staff_repository
from core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", status_code=status.HTTP_200_OK)
def login_staff(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    staff = staff_repository.get_by_email(db, form_data.username)
    
    if not staff or not verify_password(form_data.password, staff.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password parameters provided"
        )
        
    
    token_data = {"sub": str(staff.staff_id), "role": staff.role.value}
    token = create_access_token(data=token_data)
    
    return {"access_token": token, "token_type": "bearer"}
