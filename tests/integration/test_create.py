"""
Integration tests for POST /api/v1/tickets/.

Uses:
- Real FastAPI application
- Real test database
- POST endpoint only
"""

from uuid import UUID

import pytest


def valid_ticket_payload() -> dict:
    """Return a fresh, valid request body for each test."""
    return {
        "title": "Cannot log in",
        "description": "Password is being rejected",
        "priority": "high",
    }


# =========================================================
# HAPPY-PATH TESTS
# =========================================================


async def test_create_ticket_with_valid_data_returns_201(client):
    response = await client.post(
        "/api/v1/tickets/",
        json=valid_ticket_payload(),
    )

    assert response.status_code == 201

    body = response.json()

    assert body["title"] == "Cannot log in"
    assert body["description"] == "Password is being rejected"
    assert body["priority"] == "high"
    assert body["status"] == "open"


async def test_create_ticket_without_priority_defaults_to_medium(client):
    response = await client.post(
        "/api/v1/tickets/",
        json={
            "title": "Login problem",
            "description": "Customer cannot access the account",
        },
    )

    assert response.status_code == 201
    assert response.json()["priority"] == "medium"


async def test_create_ticket_without_assignee_returns_null(client):
    response = await client.post(
        "/api/v1/tickets/",
        json=valid_ticket_payload(),
    )

    assert response.status_code == 201
    assert response.json()["assignee_email"] is None


async def test_create_ticket_with_assignee_email_returns_email(client):
    payload = valid_ticket_payload()
    payload["assignee_email"] = "support@example.com"

    response = await client.post(
        "/api/v1/tickets/",
        json=payload,
    )

    assert response.status_code == 201
    assert response.json()["assignee_email"] == "support@example.com"


async def test_create_ticket_response_contains_generated_fields(client):
    response = await client.post(
        "/api/v1/tickets/",
        json=valid_ticket_payload(),
    )

    assert response.status_code == 201

    body = response.json()

    assert "id" in body
    assert "created_at" in body
    assert "updated_at" in body

    assert body["id"] is not None
    assert body["created_at"] is not None
    assert body["updated_at"] is not None


async def test_generated_ticket_id_is_valid_uuid(client):
    response = await client.post(
        "/api/v1/tickets/",
        json=valid_ticket_payload(),
    )

    assert response.status_code == 201

    ticket_id = response.json()["id"]

    # Raises ValueError if the returned ID is not a valid UUID.
    parsed_id = UUID(ticket_id)

    assert str(parsed_id) == ticket_id


async def test_create_multiple_tickets_generates_different_ids(client):
    first_response = await client.post(
        "/api/v1/tickets/",
        json={
            "title": "First problem",
            "description": "Description for the first problem",
        },
    )

    second_response = await client.post(
        "/api/v1/tickets/",
        json={
            "title": "Second problem",
            "description": "Description for the second problem",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    first_id = first_response.json()["id"]
    second_id = second_response.json()["id"]

    assert first_id != second_id


# =========================================================
# VALIDATION FAILURE TESTS
# =========================================================


async def test_create_ticket_without_title_returns_422(client):
    response = await client.post(
        "/api/v1/tickets/",
        json={
            "description": "Password is being rejected",
            "priority": "high",
        },
    )

    assert response.status_code == 422


async def test_create_ticket_without_description_returns_422(client):
    response = await client.post(
        "/api/v1/tickets/",
        json={
            "title": "Cannot log in",
            "priority": "high",
        },
    )

    assert response.status_code == 422


async def test_create_ticket_with_empty_title_returns_422(client):
    response = await client.post(
        "/api/v1/tickets/",
        json={
            "title": "",
            "description": "Password is being rejected",
        },
    )

    assert response.status_code == 422


async def test_create_ticket_with_empty_description_returns_422(client):
    response = await client.post(
        "/api/v1/tickets/",
        json={
            "title": "Cannot log in",
            "description": "",
        },
    )

    assert response.status_code == 422


async def test_create_ticket_with_whitespace_title_returns_422(client):
    response = await client.post(
        "/api/v1/tickets/",
        json={
            "title": "   ",
            "description": "Password is being rejected",
        },
    )

    assert response.status_code == 422


async def test_create_ticket_with_whitespace_description_returns_422(client):
    response = await client.post(
        "/api/v1/tickets/",
        json={
            "title": "Cannot log in",
            "description": "   ",
        },
    )

    assert response.status_code == 422


async def test_create_ticket_with_null_title_returns_422(client):
    response = await client.post(
        "/api/v1/tickets/",
        json={
            "title": None,
            "description": "Password is being rejected",
        },
    )

    assert response.status_code == 422


async def test_create_ticket_with_null_description_returns_422(client):
    response = await client.post(
        "/api/v1/tickets/",
        json={
            "title": "Cannot log in",
            "description": None,
        },
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "invalid_priority",
    [
        "urgent",
        "critical",
        "HIGH",
        "Medium",
        "",
        123,
        None,
    ],
)
async def test_create_ticket_with_invalid_priority_returns_422(
    client,
    invalid_priority,
):
    payload = valid_ticket_payload()
    payload["priority"] = invalid_priority

    response = await client.post(
        "/api/v1/tickets/",
        json=payload,
    )

    assert response.status_code == 422


async def test_create_ticket_with_empty_body_returns_422(client):
    response = await client.post(
        "/api/v1/tickets/",
        json={},
    )

    assert response.status_code == 422


async def test_create_ticket_without_json_body_returns_422(client):
    response = await client.post(
        "/api/v1/tickets/",
    )

    assert response.status_code == 422


# =========================================================
# BOUNDARY TESTS
# =========================================================


async def test_create_ticket_with_200_character_title_returns_201(client):
    payload = valid_ticket_payload()
    payload["title"] = "a" * 200

    response = await client.post(
        "/api/v1/tickets/",
        json=payload,
    )

    assert response.status_code == 201
    assert len(response.json()["title"]) == 200


async def test_create_ticket_with_title_over_200_characters_returns_422(client):
    payload = valid_ticket_payload()
    payload["title"] = "a" * 201

    response = await client.post(
        "/api/v1/tickets/",
        json=payload,
    )

    assert response.status_code == 422


async def test_create_ticket_with_5000_character_description_returns_201(client):
    payload = valid_ticket_payload()
    payload["description"] = "a" * 5000

    response = await client.post(
        "/api/v1/tickets/",
        json=payload,
    )

    assert response.status_code == 201
    assert len(response.json()["description"]) == 5000


async def test_create_ticket_with_description_over_5000_characters_returns_422(
    client,
):
    payload = valid_ticket_payload()
    payload["description"] = "a" * 5001

    response = await client.post(
        "/api/v1/tickets/",
        json=payload,
    )

    assert response.status_code == 422


async def test_create_ticket_with_assignee_over_254_characters_returns_422(
    client,
):
    payload = valid_ticket_payload()
    payload["assignee_email"] = "a" * 255

    response = await client.post(
        "/api/v1/tickets/",
        json=payload,
    )

    assert response.status_code == 422