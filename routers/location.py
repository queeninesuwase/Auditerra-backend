
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from database import get_db
from schemas.location import LocationCreate, LocationRead, LocationUpdate
from services import location_service

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/", response_model=list[LocationRead])
def list_locations(db: Session = Depends(get_db)):
    return location_service.list_locations(db)


@router.get("/{location_id}", response_model=LocationRead)
def get_location(location_id: UUID, db: Session = Depends(get_db)):
    return location_service.get_location(db, location_id)


@router.get("/county/{county}", response_model=list[LocationRead])
def get_by_county(county: str, db: Session = Depends(get_db)):
    return location_service.get_locations_by_county(db, county)


@router.get("/staff/{staff_id}", response_model=list[LocationRead])
def get_by_staff(staff_id: UUID, db: Session = Depends(get_db)):
    return location_service.get_locations_by_staff(db, staff_id)


@router.post("/", response_model=LocationRead, status_code=status.HTTP_201_CREATED)
def create_location(data: LocationCreate, db: Session = Depends(get_db)):
    return location_service.create_location(db, data)


@router.post("/capture-boundary")
def capture_boundary(
    staff_id: UUID,
    coordinates: List[dict],
    db: Session = Depends(get_db)
):
    return location_service.capture_farm_boundary(db, staff_id, coordinates)


@router.put("/{location_id}", response_model=LocationRead)
def update_location(location_id: UUID, data: LocationUpdate, db: Session = Depends(get_db)):
    return location_service.update_location(db, location_id, data)


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: UUID, db: Session = Depends(get_db)):
    location_service.delete_location(db, location_id)
    return None