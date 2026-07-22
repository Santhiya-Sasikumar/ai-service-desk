from uuid import UUID


class TicketNotFoundError(Exception):
    def __init__(self, ticket_id: UUID):
        self.ticket_id = str(ticket_id)
        super().__init__(f"Ticket {ticket_id} was not found")


class TicketStateError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)