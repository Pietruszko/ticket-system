import pytest
from django.urls import reverse
from ..models import Ticket

@pytest.mark.django_db
def test_ticket_crud_create(client):
    """Test ticket viewset creating tickets."""
    data = {
        'title': 'test',
        'body': 'test',
        'status': 'D'
    }
    url = reverse('tickets-list')
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.data['title'] == data['title']
    assert Ticket.objects.count() == 1

@pytest.mark.django_db
def test_ticket_crud_retrieve_list(client):
    """Test ticket viewset retrieving list of tickets."""
    # First create ticket object
    ticket = Ticket.objects.create(
        title='Test title',
        body='Test body',
        status='D'
    )
    url = reverse('tickets-list')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_ticket_crud_retrieve_detail(client):
    """Test ticket viewset retrieving single ticket."""
    # First create ticket object
    ticket = Ticket.objects.create(
        title='Test title',
        body='Test body',
        status='D'
    )
    url = reverse('tickets-detail', args=[ticket.id])
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_ticket_crud_update_put_patch(client):
    """Test ticket viewset fully and partially updating ticket."""
    # First create ticket object
    ticket = Ticket.objects.create(
        title='Test title',
        body='Test body',
        status='D'
    )

    # Put test
    update = {
        'title': 'New title',
        'body': 'New body',
        'status': 'O',
    }
    url = reverse('tickets-detail', args=[ticket.id])
    response = client.put(url, update, content_type='application/json')
    assert response.status_code == 200
    ticket.refresh_from_db()
    assert ticket.title == update['title']

    # Patch test
    response = client.patch(url, {'status': 'C'}, content_type='application/json')
    assert response.status_code == 200
    ticket.refresh_from_db()
    assert ticket.status == 'C'

@pytest.mark.django_db
def test_ticket_crud_delete(client):
    """Test ticket viewset deleting ticket."""
    # First create ticket object
    ticket = Ticket.objects.create(
        title='Test title',
        body='Test body',
        status='D'
    )
    url = reverse('tickets-detail', args=[ticket.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert Ticket.objects.count() == 0


