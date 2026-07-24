import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.api.tickets import router as ticket_router
from app.core.config import settings
from app.core.exceptions import TicketNotFoundError, TicketStateError
from app.db.database import engine
from app.api.ai import router   
from app.middleware.response_time import add_response_time


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.middleware("http")(add_response_time)


@app.exception_handler(TicketNotFoundError)
async def ticket_not_found_handler(
    request: Request,
    exception: TicketNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "error": "ticket_not_found",
            "id": exception.ticket_id,
        },
    )


@app.exception_handler(TicketStateError)
async def ticket_state_handler(
    request: Request,
    exception: TicketStateError,
):
    return JSONResponse(
        status_code=409,
        content={
            "error": "invalid_ticket_state",
            "message": exception.message,
        },
    )


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}


@app.get("/ready", tags=["System"])
async def readiness_check():
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

        return {
            "status": "ready",
            "database": "connected",
        }

    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "database": "unavailable",
            },
        )


app.include_router(
    ticket_router,
    prefix="/api/v1",
)
app.include_router(
    router,
    prefix="/api/v1",
    tags=["AI"],    )

