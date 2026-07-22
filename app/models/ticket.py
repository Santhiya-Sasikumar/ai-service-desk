import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class Ticket(Base):
    __tablename__ = "tickets"

    __table_args__ = (
        Index("ix_tickets_status_priority", "status", "priority"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        Enum(
            "low",
            "medium",
            "high",
            name="ticket_priority",
        ),
        nullable=False,
        default="medium",
        server_default="medium",
    )

    status: Mapped[str] = mapped_column(
        Enum(
            "open",
            "in_progress",
            "resolved",
            "closed",
            name="ticket_status",
        ),
        nullable=False,
        default="open",
        server_default="open",
    )
    assignee_email: Mapped[str | None] = mapped_column(
    String(254),
    nullable=True,
)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )