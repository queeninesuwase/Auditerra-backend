
from sqlalchemy.orm import Session
from uuid import UUID
from models.log import DiagnosticLog


class LogRepository:
    def __init__(self):
        self.model = DiagnosticLog

    def get(self, db: Session, log_id: UUID):
        return db.get(DiagnosticLog, log_id)

    def get_by_ticket(self, db: Session, ticket_id: UUID):
        return db.query(DiagnosticLog).filter(DiagnosticLog.ticket_id == ticket_id).first()

    def get_by_staff(self, db: Session, staff_id: UUID):
        return db.query(DiagnosticLog).filter(DiagnosticLog.staff_id == staff_id).all()

    def get_all(self, db: Session):
        return db.query(DiagnosticLog).all()

    def create(self, db: Session, data: dict):
        log = DiagnosticLog(**data)
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    def update(self, db: Session, db_obj: DiagnosticLog, data: dict):
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: DiagnosticLog):
        db.delete(db_obj)
        db.commit()


log_repository = LogRepository()