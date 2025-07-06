import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .. models import Ticket


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username="testuser", password="testpass123"
    )

@pytest.fixture
def authenticated_client(test_user):
    refresh = RefreshToken.for_user(test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client

@pytest.fixture
def test_ticket(test_user):
    ticket = Ticket.objects.create(
        author=test_user,
        title='Test title',
        body='Test body',
        status='D'
    )
    return ticket