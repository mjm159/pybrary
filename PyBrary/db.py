# STANDARD LIBRARY
import json
import os

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
    USER_CREATED = "USER CREATED"
    BOOK_CREATED = "BOOK CREATED"
    WISHLIST_UPDATED = "WISHLIST UPDATED"
    ALREADY_EXISTS = "ALREADY EXISTS"
    NONEXISTENT = "NONEXISTENT"
    USER_REMOVED = "USER_REMOVED"

# DECORATORS
def db_handler(table_name=None):
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


# USER RELATED FUNCTIONS
@db_handler(table_name=USERS_TABLE)
def add_user(table:TinyDB.table, first_name:str, last_name:str, email:str, password:str) -> dict:
    """Adds new user to database
    """
    if table.contains(USER.email == email):
        return make_response(Response.ALREADY_EXISTS)
    user = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password
    }
    table.insert(user)
    return make_response(Response.USER_CREATED)

@db_handler(table_name=USERS_TABLE)
def remove_user(table:TinyDB.table, email:str) -> dict:
    """Removes a user by email
    """
    if not table.contains(USER.email == email):
        return make_response(Response.NONEXISTENT)
    table.remove(USER.email == email)
    return make_response(Response.USER_REMOVED)