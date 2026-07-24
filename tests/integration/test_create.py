"""
Integration tests for POST /api/v1/tickets/
Real app, real test database, one endpoint only.
"""


async def test_create_ticket_with_valid_data_returns_201(client):
    # HAPPY: full valid payload
    response = await client.post("/api/v1/tickets/", json={
        "title": "Cannot log in",
        "description": "Password rejected",
        "priority": "high",
    })
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Cannot log in"
    assert body["status"] == "open"          # default applied by DB
    assert body["priority"] == "high"


async def test_create_ticket_without_priority_defaults_to_medium(client):
    # EDGE: priority omitted entirely
    response = await client.post("/api/v1/tickets/", json={
        "title": "t",
        "description": "d",
    })
    assert response.status_code == 201
    assert response.json()["priority"] == "medium"


async def test_create_ticket_with_empty_description_returns_422(client):
    # FAILURE: schema validation stops it before it reaches the DB
    response = await client.post("/api/v1/tickets/", json={
        "title": "t",
        "description": "",
    })
    assert response.status_code == 422


async def test_create_ticket_with_invalid_priority_returns_422(client):
    # FAILURE: "urgent" is not in the allowed Literal set
    response = await client.post("/api/v1/tickets/", json={
        "title": "t",
        "description": "d",
        "priority": "urgent",
    })
    assert response.status_code == 422


async def test_create_ticket_response_includes_generated_fields(client):
    # HAPPY: proves id/created_at/updated_at come back from the real DB
    response = await client.post("/api/v1/tickets/", json={
        "title": "t",
        "description": "d",
    })
    body = response.json()
    assert "id" in body
    assert "created_at" in body
    assert "updated_at" in body