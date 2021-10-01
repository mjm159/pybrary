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

@db.db_handler(table_name=BOOKS_TABLE)
def book_exists(table:TinyDB.table, isbn:str) -> bool:
    Book = Query()
    return table.contains(Book.isbn == isbn)

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
        password=['password'])

@pytest.fixture
def setup_database_with_n20(setup_database):
    book = TEST_BOOK['N2O']
    res = db.add_book(
        title=book['title'],
        author=book['author'],
        isbn=book['isbn'],
        publication_date=book['publication_date'])

# USERS SECTION
def test_get_user(setup_database):
    user_0 = EXAMPLE_USERS[0]
    res = db.get_user(email=user_0['email'])
    assert user_0 == res['DATA']

def test_get_all_users(setup_database):
    test_results = db.get_all_users()
    with open(config.EXAMPLE_DATA, 'r') as f:
        expected_results = json.load(f)
    assert expected_results[USERS_TABLE] == test_results['DATA']

def test_add_user(setup_database):
    user = TEST_USER['BOB']
    res = db.add_user(
        first_name=user['first_name'],
        last_name=user['last_name'],
        email=user['email'],
        password=['password'])
    assert res['STATUS'] == db.Response.USER_CREATED
    assert user_exists(email=user['email'])

def test_add_duplicate_user(setup_database_with_betty):
    user = TEST_USER['BETTY']
    assert user_exists(email=user['email'])
    res = db.add_user(
        first_name=user['first_name'],
        last_name=user['last_name'],
        email=user['email'],
        password=['password'])
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

# BOOKS SECTION
def test_get_book(setup_database):
    book_0 = EXAMPLE_BOOKS[0]
    res = db.get_book(book_0['isbn'])
    assert book_0 == res['DATA']

def test_get_all_books(setup_database):
    test_results = db.get_all_books()
    with open(config.EXAMPLE_DATA, 'r') as f:
        expected_results = json.load(f)
    assert expected_results[BOOKS_TABLE] == test_results['DATA']

def test_add_book(setup_database):
    book = TEST_BOOK['RUFF']
    res = db.add_book(
        title=book['title'],
        author=book['author'],
        isbn=book['isbn'],
        publication_date=book['publication_date'])
    assert res['STATUS'] == db.Response.BOOK_CREATED
    assert book_exists(isbn=book['isbn'])

def test_add_duplicate_book(setup_database_with_n20):
    book = TEST_BOOK['N2O']
    assert book_exists(isbn=book['isbn'])
    res = db.add_book(
        title=book['title'],
        author=book['author'],
        isbn=book['isbn'],
        publication_date=book['publication_date'])
    assert res['STATUS'] == db.Response.ALREADY_EXISTS

def test_remove_existing_book(setup_database_with_n20):
    book = TEST_BOOK['N2O']
    res = db.remove_book(isbn=book['isbn'])
    assert res['STATUS'] == db.Response.BOOK_REMOVED
    assert not book_exists(isbn=book['isbn'])

def test_remove_nonexistant_book(setup_database):
    fake_isbn = '7777777777'
    assert not book_exists(isbn=fake_isbn)
    res = db.remove_book(isbn=fake_isbn)
    assert res['STATUS'] == db.Response.NONEXISTENT

