# 3RD PARTY MODULES
from flask import Flask

# SETUP
app = Flask(__name__)

# BASELINE ENDPOINTS
@app.route("/heartbeat", methods=['GET'])
def heartbeat():
    return { "status": "OK" }

# USER ENDPOINTS
@app.route("/api/v1/users", methods=['GET', 'POST'])
def users():
    return { "status": "OK" }

@app.route("/api/v1/users/<email>", methods=['GET', 'PUT'])
def user(email):
    return { "status": "OK" }

# WISHLIST ENDPOINTS
@app.route("/api/v1/users/<email>/wishlist", methods=['GET', 'PUT'])
def wishlist(email):
    return { "status": "OK" }

# BOOK ENDPOINTS
@app.route("/api/v1/books", methods=['GET', 'POST'])
def books():
    return { "status": "OK" }

@app.route("/api/v1/books/<book>", methods=['GET', 'PUT'])
def book(book):
    return { "status": "OK" }