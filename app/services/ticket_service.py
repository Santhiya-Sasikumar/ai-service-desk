from app.schemas.ticket import TicketCreate, TicketUpdate

tickets = {}
ticket_count = 1
class TicketService:
    @staticmethod
    def create_ticket(ticket: TicketCreate):
        global ticket_count
        new_ticket = {
            "id" : ticket_count,
            "title" : ticket.title,
            "description" : ticket.description,
            "priority" : ticket.priority,
            "status" : "Open",
        }
        tickets[ticket_count] = new_ticket
        ticket_count+=1
        return new_ticket
    
    @staticmethod
    def get_all_ticket():
        return list(tickets.values())
    
    @staticmethod
    def get_ticket(ticket_id: int):
        return tickets.get(ticket_id)
    
    @staticmethod
    def update_ticket(ticket_id: int, ticket: TicketUpdate):
        exist = tickets.get(ticket_id)
        if not exist:
            return None
        update_data = ticket.model_dump(exclude_unset=True)
        exist.update(update_data)
        return exist
    
    @staticmethod
    def delete_ticket(ticket_id: int):
        return tickets.pop(ticket_id, None)