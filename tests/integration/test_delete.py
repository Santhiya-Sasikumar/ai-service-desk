"""
Integration tests for DELETE /api/v1/tickets/{id}
Real app, real test database, delete endpoint only.
"""

import uuid


async def test_delete_existing_ticket_returns_204(client):
    # HAPPY
    create = await client.post("/api/v1/tickets/", json={"title": "t", "description": "d"})
    ticket_id = create.json()["id"]

    response = await client.delete(f"/api/v1/tickets/{ticket_id}")
    assert response.status_code == 204


async def test_delete_response_has_no_body(client):
    # EDGE: 204 responses must not carry a JSON body
    create = await client.post("/api/v1/tickets/", json={"title": "t", "description": "d"})
    ticket_id = create.json()["id"]

    response = await client.delete(f"/api/v1/tickets/{ticket_id}")
    assert response.content == b""


async def test_deleted_ticket_is_actually_gone(client):
    # HAPPY: confirms the row was really removed, not just hidden
    create = await client.post("/api/v1/tickets/", json={"title": "t", "description": "d"})
    ticket_id = create.json()["id"]

    await client.delete(f"/api/v1/tickets/{ticket_id}")
    get_after = await client.get(f"/api/v1/tickets/{ticket_id}")

    assert get_after.status_code == 404


async def test_delete_nonexistent_ticket_returns_404(client):
    # FAILURE
    response = await client.delete(f"/api/v1/tickets/{uuid.uuid4()}")
    assert response.status_code == 404


async def test_delete_same_ticket_twice_second_call_returns_404(client):
    # EDGE: deleting an already-deleted ticket
    create = await client.post("/api/v1/tickets/", json={"title": "t", "description": "d"})
    ticket_id = create.json()["id"]

    first_delete = await client.delete(f"/api/v1/tickets/{ticket_id}")
    second_delete = await client.delete(f"/api/v1/tickets/{ticket_id}")

    assert first_delete.status_code == 204
    assert second_delete.status_code == 404