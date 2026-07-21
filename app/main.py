from fastapi import FastAPI
from app.api.tickets import router as ticket_router

app = FastAPI(title="AI Service Desk")

app.include_router(ticket_router)