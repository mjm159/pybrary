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
    response = client.get('/api/v1/heartbeat')
    assert response.status_code == 200

# /api/v1/users* ENDPOINT TESTS
def test_add_user(client):
    data = {
        'first_name': 'bob',
        'last_name': 'quink',
        'email': 'bobquink@bob.com',
        'password': 'bobiscool'
    }
    response = client.post('/api/v1/users', json=data)
    assert response.status_code == 200

# /api/v1/books* ENDPOINT TESTS