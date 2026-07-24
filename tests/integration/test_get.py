"""
Integration tests for GET /api/v1/tickets/ and GET /api/v1/tickets/{id}
Real app, real test database, get endpoints only.
"""

import uuid


async def test_get_all_tickets_returns_empty_list_when_none_exist(client):
    # EDGE: fresh database, nothing created yet
    response = await client.get("/api/v1/tickets/")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_all_tickets_returns_created_tickets(client):
    # HAPPY: create two, then confirm both show up
    await client.post("/api/v1/tickets/", json={"title": "a", "description": "d"})
    await client.post("/api/v1/tickets/", json={"title": "b", "description": "d"})

    response = await client.get("/api/v1/tickets/")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_all_tickets_orders_newest_first(client, db_session):
    # HAPPY: proves ORDER BY created_at DESC through the real API
    import datetime
    from app.models.ticket import Ticket
    from uuid import UUID

    first = await client.post("/api/v1/tickets/", json={"title": "first", "description": "d"})
    second = await client.post("/api/v1/tickets/", json={"title": "second", "description": "d"})

    # Since PostgreSQL's now() returns the same timestamp for all inserts in the same transaction,
    # we manually adjust the created_at timestamp of the first ticket to be in the past.
    first_id = UUID(first.json()["id"])
    first_ticket = await db_session.get(Ticket, first_id)
    first_ticket.created_at = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=10)
    await db_session.flush()

    response = await client.get("/api/v1/tickets/")
    results = response.json()
    assert results[0]["id"] == second.json()["id"]
    assert results[1]["id"] == first.json()["id"]


async def test_get_single_ticket_by_id_returns_correct_ticket(client):
    # HAPPY
    create = await client.post("/api/v1/tickets/", json={"title": "t", "description": "d"})
    ticket_id = create.json()["id"]

    response = await client.get(f"/api/v1/tickets/{ticket_id}")
    assert response.status_code == 200
    assert response.json()["id"] == ticket_id


async def test_get_ticket_with_missing_id_returns_404(client):
    # FAILURE: valid UUID format, but no matching row
    response = await client.get(f"/api/v1/tickets/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json()["error"] == "ticket_not_found"


async def test_get_ticket_with_malformed_id_returns_422(client):
    # FAILURE: not even a valid UUID, caught before reaching the service
    response = await client.get("/api/v1/tickets/not-a-uuid")
    assert response.status_code == 422