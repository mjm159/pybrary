# 3RD PARTY MODULES
from tinydb import TinyDB, Query
from flask import Flask

# LOCAL MODULES
from PyBrary import config

# SETUP
DATABASE = config.ENVIRONMENTS[config.ENV]['DATABASE']


def db_handler(func):
    def wrapper(*args, **kwargs):
        with TinyDB(DATABASE) as conn:
            return func(conn, *args, **kwargs)
    return wrapper


@db_handler
def add_user(conn:TinyDB, first_name:str, last_name:str, email:str, password:str) -> bool:
    """Adds new user to database
    """
    user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password
    }
    conn.insert(user)
    return True