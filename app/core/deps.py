from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import AsyncSessionLocal
from app.repositories.ticket_repository import TicketRepository
from app.services.ticket_service import TicketService


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def get_ticket_repository(
    session: AsyncSession = Depends(get_db),
) -> TicketRepository:
    return TicketRepository(session)


def get_ticket_service(
    repository: TicketRepository = Depends(get_ticket_repository),
) -> TicketService:
    return TicketService(repository)