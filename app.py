# STANDARD LIBRARY
import json

# 3RD PARTY MODULES
from flask import Flask, request

# LOCAL MODULES
from PyBrary import db


# SETUP
app = Flask(__name__)


# BASELINE ENDPOINTS
@app.route("/api/v1/heartbeat", methods=['GET'])
def heartbeat():
    return { "status": "OK" }

# USER ENDPOINTS
@app.route("/api/v1/users", methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        res = db.add_user(**request.json)
        if res:
            return { "status": "OK" }
        else:
            return {"status": "FAILED"}

@app.route("/api/v1/users/<id>", methods=['GET', 'PUT', 'DELETE'])
def user(id):
    return { "status": "OK" }

# WISHLIST ENDPOINTS
@app.route("/api/v1/users/<id>/wishlist", methods=['GET', 'PUT'])
def wishlist(id):
    return { "status": "OK" }

# BOOK ENDPOINTS
@app.route("/api/v1/books", methods=['GET', 'POST'])
def books():
    return { "status": "OK" }

@app.route("/api/v1/books/<isbn>", methods=['GET', 'PUT', 'DELETE'])
def book(isbn):
    return { "status": "OK" }