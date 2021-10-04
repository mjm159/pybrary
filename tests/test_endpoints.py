# STANDARD LIBRARY
import json

# 3RD PARTY MODULES
import pytest

# LOCAL MODULES
from app import app
from PyBrary import initialize_database, db, config

# GLOBALS
USERS_TABLE = config.USERS_TABLE_NAME
BOOKS_TABLE = config.BOOKS_TABLE_NAME
with open(config.EXAMPLE_DATA) as f:
    EXAMPLE_DATA = json.load(f)
EXAMPLE_USERS = EXAMPLE_DATA[USERS_TABLE]
EXAMPLE_BOOKS = EXAMPLE_DATA[BOOKS_TABLE]

# TESTING DATA
with open(config.TEST_USERS_FILE) as f:
    TEST_USER = json.load(f)
with open(config.TEST_BOOKS_FILE) as f:
    TEST_BOOK = json.load(f)

# FIXTURES
@pytest.fixture
def client():
    initialize_database(env='TEST')
    with app.test_client() as client:
        yield client

# BASELINE TESTS
def test_heartbeat(client):
    response = client.get('/api/v1/heartbeat')
    assert response.status_code == 200

# /api/v1/users* ENDPOINT TESTS
def test_get_all_users(client):
    response = client.get('/api/v1/users')
    assert response.status_code == 200

def test_get_user(client):
    test_id = "ada@firstprogrammer.com"
    response = client.get(f'/api/v1/users/{test_id}')
    assert response.status_code == 200

def test_add_user(client):
    data = TEST_USER['BETTY']
    response = client.post('/api/v1/users', json=data)
    assert response.status_code == 201

def test_update_user(client):
    email = "ada@firstprogrammer.com"
    test_key = 'last_name'
    test_val = 'test value'
    data = db.get_user(email=email)['DATA']
    data[test_key] = test_val
    response = client.put(f'/api/v1/users/{email}', json=data)
    assert response.status_code == 200

def test_remove_user(client):
    email = "ada@firstprogrammer.com"
    response = client.delete(f'/api/v1/users/{email}')
    assert response.status_code == 200

# /api/v1/users/<email>/wishlist
def test_get_wishlist(client):
    email = "alan@turingcomplete.com"
    response = client.get(f'/api/v1/users/{email}/wishlist')
    assert response.status_code == 200

def test_add_to_wishlist(client):
    email = "alan@turingcomplete.com"
    data = { "isbn": "0765308630" }
    response = client.post(f'/api/v1/users/{email}/wishlist', json=data)
    assert response.status_code == 200

def test_remove_from_wishlist(client):
    email = "alan@turingcomplete.com"
    isbn =  "0765308630"
    response = client.delete(f'/api/v1/users/{email}/wishlist/{isbn}')
    assert response.status_code == 200

# /api/v1/books* ENDPOINT TESTS
def test_get_all_books(client):
    response = client.get(f'/api/v1/books')
    assert response.status_code == 200

def test_get_book(client):
    isbn = "0765308630"
    response = client.get(f'/api/v1/books/{isbn}')
    assert response.status_code == 200

def test_add_book(client):
    data = TEST_BOOK['N2O']
    response = client.post(f'/api/v1/books', json=data)
    assert response.status_code == 201

def test_remove_book(client):
    isbn = "0765308630"
    response = client.delete(f'/api/v1/books/{isbn}')
    assert response.status_code == 200