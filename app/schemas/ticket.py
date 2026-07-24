from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


TicketPriority = Literal[
    "low",
    "medium",
    "high",
]

TicketStatus = Literal[
    "open",
    "in_progress",
    "resolved",
    "closed",
]


class TicketCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    title: str = Field(
        min_length=1,
        max_length=200,
    )

    description: str = Field(
        min_length=1,
        max_length=5000,
    )

    priority: TicketPriority = "medium"

    assignee_email: str | None = Field(
        default=None,
        max_length=254,
    )


class TicketUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=5000,
    )

    priority: TicketPriority | None = None

    status: TicketStatus | None = None

    assignee_email: str | None = Field(
        default=None,
        max_length=254,
    )


class TicketResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    title: str
    description: str
    priority: TicketPriority
    status: TicketStatus
    assignee_email: str | None
    created_at: datetime
    updated_at: datetime
class SummarizeRequest(BaseModel):
    ticket_description: str = Field(min_length=1, max_length=5_000)
 
 
class SummarizeResponse(BaseModel):
    summary: str
    suggested_response: str