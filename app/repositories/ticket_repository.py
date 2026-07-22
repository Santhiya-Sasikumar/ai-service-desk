from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate


class TicketRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, ticket_data: TicketCreate) -> Ticket:
        ticket = Ticket(**ticket_data.model_dump())

        self.session.add(ticket)
        await self.session.flush()
        await self.session.refresh(ticket)

        return ticket

    async def get_all(self) -> list[Ticket]:
        query = select(Ticket).order_by(Ticket.created_at.desc())
        result = await self.session.execute(query)

        return list(result.scalars().all())

    async def get_by_id(self, ticket_id: UUID) -> Ticket | None:
        return await self.session.get(Ticket, ticket_id)

    async def update(
        self,
        ticket: Ticket,
        ticket_data: TicketUpdate,
    ) -> Ticket:
        update_data = ticket_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        for field, value in update_data.items():
            setattr(ticket, field, value)

        await self.session.flush()
        await self.session.refresh(ticket)

        return ticket

    async def delete(self, ticket: Ticket) -> None:
        await self.session.delete(ticket)
        await self.session.flush()