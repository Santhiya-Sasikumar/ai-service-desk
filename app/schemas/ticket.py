from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


TicketPriority = Literal["low", "medium", "high"]

TicketStatus = Literal[
    "open",
    "in_progress",
    "resolved",
    "closed",
]


class TicketCreate(BaseModel):
    title: str
    description: str
    priority: TicketPriority = "medium"
    assignee_email: str | None = None

class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: TicketPriority | None = None
    status: TicketStatus | None = None
    assignee_email: str | None = None

class TicketResponse(BaseModel):
    id: UUID
    title: str
    description: str
    priority: TicketPriority
    status: TicketStatus
    created_at: datetime
    updated_at: datetime
    assignee_email: str | None
    model_config = ConfigDict(from_attributes=True)