
import pytest
from pydantic import ValidationError
from app.schemas.ticket import TicketCreate, TicketUpdate


#title 

def test_valid_title_works():
    # HAPPY
    ticket = TicketCreate(title="Login issue", description="Password rejected")
    assert ticket.title == "Login issue"

def test_title_min_length_accepts_one_character():
    # HAPPY
    ticket = TicketCreate(title="x", description="d")
    assert ticket.title == "x"

def test_title_min_length_rejects_empty_string():
    # FAILURE
    with pytest.raises(ValidationError):
        TicketCreate(title="", description="d") 

@pytest.mark.parametrize("bad_title", [
    "",         
    "   ",      
    "x" * 201,  \
])
def test_bad_titles_are_rejected(bad_title):
    with pytest.raises(ValidationError):
        TicketCreate(title=bad_title, description="valid description")
        
def test_assignee_email_rejects_string_over_max_length():
    # FAILURE: max_length=254 boundary
    with pytest.raises(ValidationError):
        TicketCreate(title="t", description="d", assignee_email="x" * 255)

def test_title_spaces_are_trimmed():
    # EDGE
    ticket = TicketCreate(title="  Login issue  ", description="desc")
    assert ticket.title == "Login issue"


# priority 

@pytest.mark.parametrize("priority", ["low", "medium", "high"])
def test_valid_priority_values(priority):
    # HAPPY
    ticket = TicketCreate(title="t", description="d", priority=priority)
    assert ticket.priority == priority


def test_priority_default_is_medium():
    # HAPPY
    ticket = TicketCreate(title="t", description="d")
    assert ticket.priority == "medium"


@pytest.mark.parametrize("bad_priority", ["urgent", "HIGH", "", 123])
def test_invalid_priority_values_rejected(bad_priority):
    # FAILURE
    with pytest.raises(ValidationError):
        TicketCreate(title="t", description="d", priority=bad_priority)


#update 

def test_update_allows_empty_body():
    # EDGE: PATCH with nothing set should still be valid
    update = TicketUpdate()
    assert update.status is None