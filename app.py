# STANDARD LIBRARY
import json
import pdb

# 3RD PARTY MODULES
from flask import Flask, request

# LOCAL MODULES
from PyBrary import db


# SETUP
app = Flask(__name__)

STATUS_CODE = {
    db.Response.SUCCESS: 200,
    db.Response.FAILURE: 500,
    db.Response.USER_CREATED: 201,
    db.Response.USER_UPDATED: 200,
    db.Response.USER_REMOVED: 200,
    db.Response.USER_NONEXISTENT: 404,
    db.Response.USER_ALREADY_EXISTS: 406,
    db.Response.BOOK_CREATED: 201,
    db.Response.BOOK_UPDATED: 200,
    db.Response.BOOK_REMOVED: 200,
    db.Response.BOOK_NONEXISTENT: 404,
    db.Response.BOOK_ALREADY_EXISTS: 406,
    db.Response.WISHLIST_UPDATED: 200
}

# BASELINE ENDPOINTS
@app.route("/api/v1/heartbeat", methods=['GET'])
def heartbeat():
    return { "status": "OK" }, 200

# USER ENDPOINTS
@app.route("/api/v1/users", methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        action_results = db.get_all_users()
    elif request.method == 'POST':
        data = request.json
        action_results = db.add_user(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password'],
                wishlist=data['wishlist'])
    return action_results, STATUS_CODE[action_results['STATUS']]

@app.route("/api/v1/users/<email>", methods=['GET', 'PUT', 'DELETE'])
def user(email):
    if request.method == 'GET':
        action_results = db.get_user(email=email)
    elif request.method == 'PUT':
        data = request.json
        action_results = db.update_user(email=email, data=data)
    elif request.method == 'DELETE':
        action_results = db.remove_user(email=email)
    return action_results, STATUS_CODE[action_results['STATUS']]

# WISHLIST ENDPOINTS
@app.route("/api/v1/users/<email>/wishlist", methods=['GET', 'POST'])
def wishlist(email):
    """Interact with user's wishlist
    
    POST - add item to wishlist
    data = { 'isbn': '9828302754' }
    """
    if request.method == 'GET':
        action_results = db.get_wishlist(email=email)
    elif request.method == 'POST':
        action_results = db.add_to_wishlist(email=email, isbn=request.json['isbn'])
    return action_results, STATUS_CODE[action_results['STATUS']]

@app.route("/api/v1/users/<email>/wishlist/<isbn>", methods=['DELETE'])
def remove_from_wishlist(email, isbn):
    action_results = db.remove_from_wishlist(email=email, isbn=isbn)
    return action_results, STATUS_CODE[action_results['STATUS']]

# BOOK ENDPOINTS
@app.route("/api/v1/books", methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        action_results = db.get_all_books()
    elif request.method == 'POST':
        data = request.json
        action_results = db.add_book(
                title=data['title'],
                author=data['author'],
                isbn=data['isbn'],
                publication_date=data['publication_date'])
    return action_results, STATUS_CODE[action_results['STATUS']]

@app.route("/api/v1/books/<isbn>", methods=['GET', 'DELETE'])
def book(isbn):
    if request.method == 'GET':
        action_results = db.get_book(isbn=isbn)
    elif request.method == 'DELETE':
        action_results = db.remove_book(isbn=isbn)
    return action_results, STATUS_CODE[action_results['STATUS']]