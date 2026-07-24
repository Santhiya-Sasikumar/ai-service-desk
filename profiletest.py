import asyncio
import cProfile
import pstats
import io
 
from app.db.database import AsyncSessionLocal
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.services.ticket_service import TicketService
from app.repositories.ticket_repository import TicketRepository
 
 
async def test_crud():


 
    # Create database session
    async with AsyncSessionLocal() as db:
 
        repository = TicketRepository(db)

        service = TicketService(repository)
 
        # ==========================================
        # 1. CREATE TICKET
        # ==========================================
        print("\n1. Creating ticket...")
 
        create_data = TicketCreate(
            title="cProfile Test",
            description="Testing service performance",
            priority="high",
        )
 
        created_ticket = await service.create_ticket(create_data)
 
        print("Created Ticket ID:", created_ticket.id)
 
        ticket_id = created_ticket.id
 
 
        # ==========================================
        # 2. GET ALL TICKETS
        # ==========================================
        print("\n2. Getting all tickets...")
 
        tickets = await service.get_all_tickets()
 
        print("Total tickets:", len(tickets))
 
 
        # ==========================================
        # 3. GET SINGLE TICKET
        # ==========================================
        print("\n3. Getting single ticket...")
 
        ticket = await service.get_ticket(ticket_id)
 
        print("Ticket ID:", ticket.id)
 
 
        # ==========================================
        # 4. UPDATE TICKET
        # ==========================================
        print("\n4. Updating ticket...")
 
        update_data = TicketUpdate(
            title="Updated cProfile Test"
        )
 
        updated_ticket = await service.update_ticket(
            ticket_id,
            update_data
        )
 
        print("Updated Ticket ID:", updated_ticket.id)
 
 
        # ==========================================
        # 5. DELETE TICKET
        # ==========================================
        print("\n5. Deleting ticket...")
 
        await service.delete_ticket(ticket_id)
 
        print("Ticket deleted successfully")
 
 
def main():
 
    # Create cProfile profiler
    profiler = cProfile.Profile()
 
    # Start profiling
    profiler.enable()
 
    # Run async CRUD operations
    asyncio.run(test_crud())
 
    # Stop profiling
    profiler.disable()
 
 
    # ==========================================
    # DISPLAY CPROFILE RESULTS
    # ==========================================
 
    stream = io.StringIO()
 
    stats = pstats.Stats(
        profiler,
        stream=stream
    )
 
    # Remove unnecessary directory paths
    stats.strip_dirs()
 
    # Sort by total cumulative execution time
    stats.sort_stats("cumulative")
 
    # Display top 30 functions
    stats.print_stats(30)
 
    print("\n")
    print("=" * 80)
    print("CPROFILE RESULTS")
    print("=" * 80)
 
    print(stream.getvalue())
 
 
if __name__ == "__main__":
    main()