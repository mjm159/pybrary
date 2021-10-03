# STANDARD LIBRARY
import json
import os
import pdb

# 3RD PARTY MODULES
from flask import Flask
from tinydb import TinyDB, Query

# LOCAL MODULES
from PyBrary import config

# SETUP
DATABASE = config.ENVIRONMENTS[config.ENV]['DATABASE']
EXAMPLE_DATA = config.EXAMPLE_DATA
USER = Query()
BOOK = Query()
USERS_TABLE = config.USERS_TABLE_NAME
BOOKS_TABLE = config.BOOKS_TABLE_NAME

# RESPONSE DEFINITIONS
class Response:
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    USER_CREATED = "USER CREATED"
    BOOK_CREATED = "BOOK CREATED"
    WISHLIST_UPDATED = "WISHLIST UPDATED"
    ALREADY_EXISTS = "ALREADY EXISTS"
    NONEXISTENT = "NONEXISTENT"
    USER_REMOVED = "USER REMOVED"
    BOOK_REMOVED = "BOOK REMOVED"

# DECORATORS
def db_handler(table_name=None):
    """Sets up and returns a connection with the database
    """
    def inner(func):
        def wrapper(*args, **kwargs):
            with TinyDB(DATABASE) as conn:
                if table_name == USERS_TABLE:
                    table = conn.table(table_name)
                elif table_name == BOOKS_TABLE:
                    table = conn.table(table_name)
                else:
                    table = conn
                return func(table, *args, **kwargs)
        return wrapper
    return inner


# UTILITY FUNCTIONS
def make_response(status:str, data:dict=None) -> dict:
    """Generates a response dictionary
    """
    return {'STATUS': status, 'DATA': data}


# USERS SECTION
@db_handler(table_name=USERS_TABLE)
def get_user(table:TinyDB.table, email:str) -> dict:
    """Get user details
    """
    if not table.contains(USER.email == email):
        return make_response(status=Response.NONEXISTENT)
    data = table.get(USER.email == email)
    return make_response(status=Response.SUCCESS, data=data)

@db_handler(table_name=USERS_TABLE)
def get_all_users(table:TinyDB.table) -> dict:
    """Returns a dict with all users in DB
    """
    return make_response(status=Response.SUCCESS, data=table.all())

@db_handler(table_name=USERS_TABLE)
def add_user(table:TinyDB.table, first_name:str, last_name:str, email:str, password:str) -> dict:
    """Adds new user to database
    """
    if table.contains(USER.email == email):
        return make_response(status=Response.ALREADY_EXISTS)
    user = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password
    }
    table.insert(user)
    return make_response(status=Response.USER_CREATED)

@db_handler(table_name=USERS_TABLE)
def update_user(table:TinyDB.table, email:str, data:dict) -> dict:
    """Update user fields

    for `data`, expecting a dict representing a user, e.g.:
        {
            "first_name": "Ada",
            "last_name": "Lovelace",
            "email": "ada@firstprogrammer.com",
            "password": "BabbageEngine",
            "wishlist": []
        }
    """
    if not table.contains(USER.email == email):
        return make_response(status=Response.NONEXISTENT)
    result = table.update(data, USER.email == email)
    if result[0] == 1:
        return make_response(status=Response.SUCCESS)
    else:
        return make_response(status=Response.FAILURE)

@db_handler(table_name=USERS_TABLE)
def remove_user(table:TinyDB.table, email:str) -> dict:
    """Removes a user by email
    """
    if not table.contains(USER.email == email):
        return make_response(status=Response.NONEXISTENT)
    table.remove(USER.email == email)
    return make_response(status=Response.USER_REMOVED)

# WISHLIST SECTION
@db_handler(table_name=BOOKS_TABLE)
def get_wishlist(table:TinyDB.table, email:str) -> dict:
    """Retrieve wishlist for specific user
    """
    user = get_user(email=email)
    status = user['STATUS']
    if status == Response.NONEXISTENT:
        return make_response(status=status)
    return make_response(status=Response.SUCCESS, data=user['DATA']['wishlist'])

@db_handler(table_name=BOOKS_TABLE)
def add_to_wishlist(table:TinyDB.table, email:str, isbn:str) -> dict:
    """Add book to user's wishlist
    """
    pass

# BOOKS SECTION
@db_handler(table_name=BOOKS_TABLE)
def get_book(table:TinyDB.table, isbn:str) -> dict:
    """Get book details
    """
    if not table.contains(BOOK.isbn == isbn):
        return make_response(status=Response.NONEXISTENT)
    data = table.get(BOOK.isbn == isbn)
    return make_response(status=Response.SUCCESS, data=data)

@db_handler(table_name=BOOKS_TABLE)
def get_all_books(table:TinyDB.table) -> dict:
    """Returns a dict with all books in DB
    """
    return make_response(status=Response.SUCCESS, data=table.all())

@db_handler(table_name=BOOKS_TABLE)
def add_book(table:TinyDB.table, title:str, author:str, isbn:str, publication_date:str) -> dict:
    """Adds new book to database
    """
    if table.contains(BOOK.isbn == isbn):
        return make_response(status=Response.ALREADY_EXISTS)
    book = {
        'title': title,
        'author': author,
        'isbn': isbn,
        'publication_date': publication_date
    }
    table.insert(book)
    return make_response(status=Response.BOOK_CREATED)

@db_handler(table_name=BOOKS_TABLE)
def remove_book(table:TinyDB.table, isbn:str) -> dict:
    """Removes a book by isbn
    """
    if not table.contains(BOOK.isbn == isbn):
        return make_response(status=Response.NONEXISTENT)
    table.remove(BOOK.isbn == isbn)
    return make_response(status=Response.BOOK_REMOVED)