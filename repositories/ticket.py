
from sqlalchemy.orm import Session
from uuid import UUID
from models.ticket import ServiceTicket


class TicketRepository:
    def __init__(self):
        self.model = ServiceTicket

    def get(self, db: Session, ticket_id: UUID):
        return db.get(ServiceTicket, ticket_id)

    def get_by_farmer(self, db: Session, farmer_id: UUID):
        return db.query(ServiceTicket).filter(ServiceTicket.farmer_id == farmer_id).all()

    def get_by_staff(self, db: Session, staff_id: UUID):
        return db.query(ServiceTicket).filter(ServiceTicket.staff_id == staff_id).all()

    def get_by_status(self, db: Session, status: str):
        return db.query(ServiceTicket).filter(ServiceTicket.status == status).all()

    def get_all(self, db: Session):
        return db.query(ServiceTicket).all()

    def create(self, db: Session, data: dict):
        ticket = ServiceTicket(**data)
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket

    def update(self, db: Session, db_obj: ServiceTicket, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: ServiceTicket):
        db.delete(db_obj)
        db.commit()


ticket_repository = TicketRepository()