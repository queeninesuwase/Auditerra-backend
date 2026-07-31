
from fastapi import FastAPI
from database import Base, engine

from models import farmer, staff, location, ticket, log, recommendation
from routers import auth as auth_router
from routers import (
    farmer as farmer_router,
    staff as staff_router,
    location as location_router,
    ticket as ticket_router,
    log as log_router,
    recommendation as recommendation_router,
    dispatch as dispatch_router,
)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auditerra API", version="2")


app.include_router(auth_router.router)
app.include_router(farmer_router.router)
app.include_router(staff_router.router)
app.include_router(location_router.router)
app.include_router(ticket_router.router)
app.include_router(log_router.router)
app.include_router(recommendation_router.router)
app.include_router(dispatch_router.router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Audittera Soil Diagnostics and Restoration Platform Gateway Engine"
    }