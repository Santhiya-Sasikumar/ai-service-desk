from locust import HttpUser, between, task
 
 
class TicketApiUser(HttpUser):
    host="http://localhost:8000"
    wait_time = between(1, 3)
 
    @task(3)
    def check_health(self) -> None:
        self.client.get("/health", name="GET /health")
 
    @task(2)
    def list_tickets(self) -> None:
        self.client.get("/api/v1/tickets/", name="GET /tickets")
 
    @task(1)
    def create_ticket(self) -> None:
        self.client.post(
            "/api/v1/tickets",
            name="POST  api/v1/tickets/",
            json={
                "title": "Load test ticket",
                "description": "A realistic ticket created by a simulated user.",
                "priority": "medium",
                "customer_type": "mail@gmail.com",
            },
        )
 