from uuid import UUID

from app.core.exceptions import (
    TicketNotFoundError,
    TicketStateError,
)
from app.models.ticket import Ticket
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket import TicketCreate, TicketUpdate


class TicketService:
    def __init__(
        self,
        repository: TicketRepository,
    ):
        self.repository = repository

    async def create_ticket(
        self,
        ticket_data: TicketCreate,
    ) -> Ticket:
        create_data = ticket_data.model_dump()

        return await self.repository.create(
            create_data
        )

    async def get_all_tickets(
        self,
    ) -> list[Ticket]:
        return await self.repository.get_all()

    async def get_ticket(
        self,
        ticket_id: UUID,
    ) -> Ticket:
        ticket = await self.repository.get_by_id(
            ticket_id
        )

        if ticket is None:
            raise TicketNotFoundError(ticket_id)

        return ticket

    async def update_ticket(
        self,
        ticket_id: UUID,
        ticket_data: TicketUpdate,
    ) -> Ticket:
        ticket = await self.get_ticket(ticket_id)

        if (
            ticket.status == "closed"
            and ticket_data.status is not None
            and ticket_data.status != "closed"
        ):
            raise TicketStateError(
                "A closed ticket cannot be reopened"
            )

        update_data = ticket_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        return await self.repository.update(
            ticket,
            update_data,
        )

    async def delete_ticket(
        self,
        ticket_id: UUID,
    ) -> None:
        ticket = await self.get_ticket(ticket_id)

        await self.repository.delete(ticket)