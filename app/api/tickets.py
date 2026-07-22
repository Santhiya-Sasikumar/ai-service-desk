from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.deps import get_ticket_service
from app.schemas.ticket import (
    TicketCreate,
    TicketResponse,
    TicketUpdate,
)
from app.services.ticket_service import TicketService


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.post(
    "/",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ticket(
    ticket_data: TicketCreate,
    service: TicketService = Depends(get_ticket_service),
):
    return await service.create_ticket(ticket_data)


@router.get(
    "/",
    response_model=list[TicketResponse],
)
async def get_all_tickets(
    service: TicketService = Depends(get_ticket_service),
):
    return await service.get_all_tickets()


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
)
async def get_ticket(
    ticket_id: UUID,
    service: TicketService = Depends(get_ticket_service),
):
    return await service.get_ticket(ticket_id)


@router.patch(
    "/{ticket_id}",
    response_model=TicketResponse,
)
async def update_ticket(
    ticket_id: UUID,
    ticket_data: TicketUpdate,
    service: TicketService = Depends(get_ticket_service),
):
    return await service.update_ticket(ticket_id, ticket_data)


@router.delete("/{ticket_id}")
async def delete_ticket(
    ticket_id: UUID,
    service: TicketService = Depends(get_ticket_service),
):
    await service.delete_ticket(ticket_id)

    return {
        "message": "Ticket deleted successfully",
        "ticket_id": str(ticket_id),
    }