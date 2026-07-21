from fastapi import APIRouter, HTTPException

from app.schemas.ticket import TicketCreate, TicketUpdate, Ticket
from app.services.ticket_service import TicketService

router = APIRouter(prefix="/tickets")

@router.post("/", response_model=Ticket)
def create_ticket(ticket: TicketCreate):
    return TicketService.create_ticket(ticket)

@router.get("/", response_model=list[Ticket])
def get_all_tickets():
    return TicketService.get_all_ticket()

@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int):
    ticket = TicketService.get_ticket(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.put("/{ticket_id}", response_model=Ticket)
def update_ticket(ticket_id: int, ticket: TicketUpdate):
    updated = TicketService.update_ticket(ticket_id, ticket)
    if updated is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return updated

@router.delete("/{ticket_id}")
def delete(ticket_id: int):
    remove = TicketService.delete_ticket(ticket_id)
    if remove is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket deleted successfully"}
