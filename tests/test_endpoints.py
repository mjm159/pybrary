# 3RD PARTY MODULES
import pytest

# LOCAL MODULES
from app import app

# FIXTURES
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# BASELINE TESTS
def test_heartbeat(client):
    response = client.get('/heartbeat')
    assert response.status_code == 200

# /api/v1/users* ENDPOINT TESTS

# /api/v1/books* ENDPOINT TESTS