# STANDARD LIBRARY
import json
import os

# 3RD PARTY MODULES
from tinydb import TinyDB, Query

# LOCAL MODULES
from PyBrary import config


# GLOBAL
ENV = config.ENV
DATABASE = config.ENVIRONMENTS[ENV]['DATABASE']
EXAMPLE_DATA = config.EXAMPLE_DATA
USERS = config.USERS_TABLE_NAME
BOOKS = config.BOOKS_TABLE_NAME

# UTILITY FUNCTIONS
def initialize_database(env:str=None) -> bool:
    """Initializes environments database to only contain contents of 'example_data.json'
    """
    if env:
        db_path = config.ENVIRONMENTS[env]['DATABASE']
    else:
        db_path = DATABASE
    if os.path.exists(db_path):
        os.remove(db_path)
    with TinyDB(db_path) as database:
        with open(EXAMPLE_DATA) as f:
            data = json.load(f)
        # USERS
        users_table = database.table(USERS)
        users_table.insert_multiple(data[USERS])
        # BOOKS
        books_table = database.table(BOOKS)
        books_table.insert_multiple(data[BOOKS])
    return True