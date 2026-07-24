from __future__ import annotations
 
from dataclasses import dataclass
 
 
@dataclass(frozen=True)
class PromptTemplate:
    name: str
    version: str
    template: str
 
    def render(self, **values: str) -> str:
        return self.template.format(**values)
 
 
TICKET_SUMMARY_V1 = PromptTemplate(
    name="ticket_summary",
    version="1.0.0",
    template=(
        "Return only in simple test "
        "First, summarize the following support ticket in a concise and professional manner. "
        "Then, suggest a brief and appropriate response to the ticket. "
        ""
        "Summarize the following support ticket and suggest a concise, "
        "professional response. Ticket: {ticket_description}"
    ),
)
 