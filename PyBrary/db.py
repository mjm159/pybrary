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
    # GENERAL
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    # USER
    USER_CREATED = "USER CREATED"
    USER_NONEXISTENT = "USER DOES NOT EXIST"
    USER_ALREADY_EXISTS = "USER ALREADY EXISTS"
    USER_REMOVED = "USER REMOVED"
    USER_UPDATED = "USER UPDATED"
    # BOOK
    BOOK_CREATED = "BOOK CREATED"
    BOOK_NONEXISTENT = "BOOK DOES NOT EXIST"
    BOOK_ALREADY_EXISTS = "BOOK ALREADY EXISTS"
    BOOK_REMOVED = "BOOK REMOVED"
    # WISHLIST
    WISHLIST_UPDATED = "WISHLIST UPDATED"

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
        return make_response(status=Response.USER_NONEXISTENT)
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
        return make_response(status=Response.USER_ALREADY_EXISTS)
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
        return make_response(status=Response.USER_NONEXISTENT)
    result = table.update(data, USER.email == email)
    return make_response(status=Response.USER_UPDATED)

@db_handler(table_name=USERS_TABLE)
def remove_user(table:TinyDB.table, email:str) -> dict:
    """Removes a user by email
    """
    if not table.contains(USER.email == email):
        return make_response(status=Response.USER_NONEXISTENT)
    table.remove(USER.email == email)
    return make_response(status=Response.USER_REMOVED)

# WISHLIST SECTION
@db_handler(table_name=USERS_TABLE)
def get_wishlist(table:TinyDB.table, email:str) -> dict:
    """Retrieve wishlist for specific user
    """
    user_search_results = get_user(email=email)
    if user_search_results['STATUS'] == Response.USER_NONEXISTENT:
        return user_search_results
    return make_response(status=Response.SUCCESS, data=user_search_results['DATA']['wishlist'])

@db_handler(table_name=USERS_TABLE)
def add_to_wishlist(table:TinyDB.table, email:str, isbn:str) -> dict:
    """Add book to user's wishlist
    """
    user_search_results = get_user(email=email)
    if user_search_results['STATUS'] != Response.SUCCESS:
        return user_search_results
    book_search_results = get_book(isbn=isbn)
    if book_search_results['STATUS'] != Response.SUCCESS:
        return book_search_results
    book_title = book_search_results['DATA']['title']
    user_data = user_search_results['DATA']
    user_data['wishlist'].setdefault(isbn, book_title)
    update_results = update_user(email=email, data=user_data)
    if update_results['STATUS'] == Response.USER_UPDATED:
        return make_response(status=Response.WISHLIST_UPDATED)
    return update_results

@db_handler(table_name=USERS_TABLE)
def remove_from_wishlist(table:TinyDB.table, email:str, isbn:str) -> dict:
    """Remove book from user's wishlist
    """
    user_search_results = get_user(email=email)
    if user_search_results['STATUS'] != Response.SUCCESS:
        return user_search_results
    user_data = user_search_results['DATA']
    user_data['wishlist'].pop(isbn, None)
    update_results = update_user(email=email, data=user_data)
    if update_results['STATUS'] == Response.USER_UPDATED:
        return make_response(status=Response.WISHLIST_UPDATED)
    return update_results

# BOOKS SECTION
@db_handler(table_name=BOOKS_TABLE)
def get_book(table:TinyDB.table, isbn:str) -> dict:
    """Get book details
    """
    if not table.contains(BOOK.isbn == isbn):
        return make_response(status=Response.BOOK_NONEXISTENT)
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
        return make_response(status=Response.BOOK_ALREADY_EXISTS)
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
        return make_response(status=Response.BOOK_NONEXISTENT)
    table.remove(BOOK.isbn == isbn)
    return make_response(status=Response.BOOK_REMOVED)