from fastapi import FastAPI
from database import Base, engine


from models import expert, farmer, location, log, recommendation, supervisor, ticket


from routers import (
    expert as expert_router,
    farmer as farmer_router,
    location as location_router,
    log as log_router,
    recommendation as recommendation_router,
    supervisor as supervisor_router,
    ticket as ticket_router,
)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auditerra API", version="1")


app.include_router(farmer_router.router)
app.include_router(expert_router.router)
app.include_router(supervisor_router.router)
app.include_router(location_router.router)
app.include_router(ticket_router.router)
app.include_router(log_router.router)
app.include_router(recommendation_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Audittera Soil Diagnostics and Restoration API Gateway"}
