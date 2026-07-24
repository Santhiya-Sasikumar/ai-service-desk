"""
Integration tests for PATCH /api/v1/tickets/{id}
Real app, real test database, update endpoint only.
"""

import uuid


async def test_update_single_field_changes_only_that_field(client):
    # HAPPY: PATCH semantics — only priority changes, title stays the same
    create = await client.post("/api/v1/tickets/", json={
        "title": "original title", "description": "d", "priority": "low",
    })
    ticket_id = create.json()["id"]

    response = await client.patch(f"/api/v1/tickets/{ticket_id}", json={"priority": "high"})

    assert response.status_code == 200
    body = response.json()
    assert body["priority"] == "high"
    assert body["title"] == "original title"  # unchanged


async def test_update_nonexistent_ticket_returns_404(client):
    # FAILURE
    response = await client.patch(
        f"/api/v1/tickets/{uuid.uuid4()}", json={"priority": "high"}
    )
    assert response.status_code == 404


async def test_update_with_empty_body_returns_200_and_no_changes(client):
    # EDGE: PATCH with nothing set should succeed and change nothing
    create = await client.post("/api/v1/tickets/", json={"title": "t", "description": "d"})
    ticket_id = create.json()["id"]

    response = await client.patch(f"/api/v1/tickets/{ticket_id}", json={})

    assert response.status_code == 200
    assert response.json()["title"] == "t"


async def test_closing_an_open_ticket_succeeds(client):
    # HAPPY: BUSINESS RULE — closing is always allowed
    create = await client.post("/api/v1/tickets/", json={"title": "t", "description": "d"})
    ticket_id = create.json()["id"]

    response = await client.patch(f"/api/v1/tickets/{ticket_id}", json={"status": "closed"})
    assert response.status_code == 200
    assert response.json()["status"] == "closed"


async def test_reopening_a_closed_ticket_returns_409(client):
    # FAILURE / BUSINESS RULE
    create = await client.post("/api/v1/tickets/", json={"title": "t", "description": "d"})
    ticket_id = create.json()["id"]

    await client.patch(f"/api/v1/tickets/{ticket_id}", json={"status": "closed"})
    reopen = await client.patch(f"/api/v1/tickets/{ticket_id}", json={"status": "open"})

    assert reopen.status_code == 409
    assert reopen.json()["error"] == "invalid_ticket_state"