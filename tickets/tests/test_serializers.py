import pytest
from ..serializers import TicketSerializer
from ..models import Ticket

@pytest.mark.django_db
def test_ticket_serializer_valid_data():
    """Test normal serializer behaviour with valid data."""
    data = {
        'title': 'Test ticket',
        'body': 'This is a valid test body of a ticket',
        'status': 'O',
    }
    serializer = TicketSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    ticket = serializer.save()
    assert ticket.title == data['title']
    assert ticket.body == data['body']
    assert ticket.status == data['status']
    assert Ticket.objects.count() == 1

@pytest.mark.django_db
def test_ticket_serializer_missing_data():
    """Test serializer not valid with missing title."""
    data = {
        # 'title': 'Test ticket', <- Missing data
        'body': 'This is a valid test body of a ticket',
        'status': 'O',
    }
    serializer = TicketSerializer(data=data)
    assert not serializer.is_valid(), serializer.errors
    assert 'title' in serializer.errors
    assert Ticket.objects.count() == 0

@pytest.mark.django_db
def test_ticket_serializer_incorrect_status():
    """Test serializer raise serializer error with wrong status for new ticket."""
    data = {
        'title': 'Test ticket',
        'body': 'This is a valid test body of a ticket',
        'status': 'I',
    }
    serializer = TicketSerializer(data=data)
    serializer.is_valid(), serializer.errors
    assert Ticket.objects.count() == 0

@pytest.mark.django_db
def test_ticket_serializer_updating_status():
    """Test serializer when changing status to correct and then incorrect one."""
    # First create ticket object
    ticket = Ticket.objects.create(
        title='Test title',
        body='Test body',
        status='D' # Starting with Draft
    )

    # Draft to Open - valid
    serializer = TicketSerializer(instance=ticket, data={'status': 'O'}, partial=True)
    assert serializer.is_valid(), serializer.errors
    serializer.save()
    assert ticket.status == 'O'

    # Open to Closed - valid
    serializer = TicketSerializer(instance=ticket, data={'status': 'C'}, partial=True)
    assert serializer.is_valid(), serializer.errors
    serializer.save()
    assert ticket.status == 'C'

    # Closed to Open - invalid
    serializer = TicketSerializer(instance=ticket, data={'status': 'O'}, partial=True)
    assert not serializer.is_valid(), serializer.errors
    assert serializer.errors