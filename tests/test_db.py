# STANDARD LIBRARY
import json
import pdb

# 3RD PARTY MODULES
import pytest
from tinydb import TinyDB, Query

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

# UTILITY FUNCTIONS
@db.db_handler(table_name=USERS_TABLE)
def user_exists(table:TinyDB.table, email:str) -> bool:
    User = Query()
    return table.contains(User.email == email)

@db.db_handler(table_name=USERS_TABLE)
def list_all_users(table:TinyDB) -> dict:
    """List all resources in a table
    """
    return table.all()


# FIXTURE DEFINITIONS
@pytest.fixture
def setup_database():
    initialize_database('TEST')

@pytest.fixture
def setup_database_with_betty(setup_database):
    user = TEST_USER['BETTY']
    res = db.add_user(
        first_name=user['first_name'],
        last_name=user['last_name'],
        email=user['email'],
        password=['password']
        )

# USERS SECTION
def test_add_user(setup_database):
    user = TEST_USER['BOB']
    res = db.add_user(
        first_name=user['first_name'],
        last_name=user['last_name'],
        email=user['email'],
        password=['password']
        )
    assert res['STATUS'] == db.Response.USER_CREATED
    assert user_exists(email=user['email'])

def test_add_duplicate_user(setup_database_with_betty):
    user = TEST_USER['BETTY']
    res = db.add_user(
        first_name=user['first_name'],
        last_name=user['last_name'],
        email=user['email'],
        password=['password']
        )
    assert res['STATUS'] == db.Response.ALREADY_EXISTS
    
def test_remove_existing_user(setup_database_with_betty):
    user = TEST_USER['BETTY']
    res = db.remove_user(email=user['email'])
    assert res['STATUS'] == db.Response.USER_REMOVED
    assert not user_exists(email=user['email'])

def test_remove_nonexistant_user(setup_database):
    fake_email = 'faker_fakerstein@fake.fk'
    assert not user_exists(email=fake_email)
    res = db.remove_user(email=fake_email)
    assert res['STATUS'] == db.Response.NONEXISTENT

def test_get_all_users(setup_database):
    test_results = db.get_all_users()
    with open(config.EXAMPLE_DATA, 'r') as f:
        expected_results = json.load(f)
    assert expected_results[USERS_TABLE] == test_results['DATA']


# BOOKS SECTION
