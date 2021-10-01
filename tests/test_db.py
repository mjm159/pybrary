# STANDARD LIBRARY
import json

# 3RD PARTY MODULES
import pytest
from tinydb import TinyDB

# LOCAL MODULES
from PyBrary import config, db, initialize_database


# GLOBAL
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


# FIXTURE DEFINITIONS
@pytest.fixture
def setup_database():
    initialize_database('TEST')

# USER SECTION
def test_add_user(setup_database):
    user = TEST_USER['BOB']
    res = db.add_user(
        first_name=user['first_name'],
        last_name=user['last_name'],
        email=user['email'],
        password=['password']
        )
    assert res['STATUS'] == db.Response.USER_CREATED

def test_add_duplicate_user(setup_database):
    user = TEST_USER['AGATHA']
    res = db.add_user(
        first_name=user['first_name'],
        last_name=user['last_name'],
        email=user['email'],
        password=['password']
        )
    assert res['STATUS'] == db.Response.USER_CREATED  
    res = db.add_user(
        first_name=user['first_name'],
        last_name=user['last_name'],
        email=user['email'],
        password=['password']
        )
    assert res['STATUS'] == db.Response.ALREADY_EXISTS
    
