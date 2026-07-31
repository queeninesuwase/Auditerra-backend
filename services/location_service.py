
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from repositories.location import location_repository
from repositories.staff import staff_repository
from schemas.location import LocationCreate, LocationUpdate


def get_location(db: Session, location_id: UUID):
    location = location_repository.get(db, location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location entry not found"
        )
    return location


def list_locations(db: Session):
    return location_repository.get_all(db)


def get_locations_by_county(db: Session, county: str):
    return location_repository.get_by_county(db, county)


def get_locations_by_staff(db: Session, staff_id: UUID):
    return location_repository.get_by_staff(db, staff_id)


def create_location(db: Session, data: LocationCreate):
    if data.latitude is not None and not (-90 <= data.latitude <= 90):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Latitude must be between -90 and 90"
        )
    if data.longitude is not None and not (-180 <= data.longitude <= 180):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Longitude must be between -180 and 180"
        )
    if data.staff_id:
        staff = staff_repository.get(db, data.staff_id)
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Referencing staff member not found"
            )
    payload = data.model_dump()
    if not payload.get("created_at"):
        payload["created_at"] = datetime.now(timezone.utc)
    return location_repository.create(db, payload)


def update_location(db: Session, location_id: UUID, data: LocationUpdate):
    location = get_location(db, location_id)
    payload = data.model_dump(exclude_unset=True)
    if "latitude" in payload and not (-90 <= payload["latitude"] <= 90):
        raise HTTPException(status_code=400, detail="Invalid latitude")
    if "longitude" in payload and not (-180 <= payload["longitude"] <= 180):
        raise HTTPException(status_code=400, detail="Invalid longitude")
    return location_repository.update(db, location, payload)


def delete_location(db: Session, location_id: UUID):
    location = get_location(db, location_id)
    location_repository.delete(db, location)


def capture_farm_boundary(db: Session, staff_id: UUID, coordinates: list):
    staff = staff_repository.get(db, staff_id)
    if not staff or staff.role != "field_expert":
        raise HTTPException(status_code=403, detail="Only field experts can capture boundaries")
    if len(coordinates) < 3:
        raise HTTPException(status_code=400, detail="At least 3 coordinate points required for a polygon")

    created_locations = []
    for coord in coordinates:
        loc_data = LocationCreate(
            latitude=coord["latitude"],
            longitude=coord["longitude"],
            staff_id=staff_id,
            county=coord.get("county"),
            country=coord.get("country"),
            country_code=coord.get("country_code"),
            region_name=coord.get("region_name"),
            postal_code=coord.get("postal_code"),
            captured_at=coord.get("captured_at")
        )
        created_locations.append(create_location(db, loc_data))
    return created_locations