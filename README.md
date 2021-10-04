# Pybrary

## Installation & Setup
In the `takehome` folder, run the following:
```bash
>> python3 -m venv ./venv
>> source venv/bin/activate
>> pip3 install -r requirements.txt
```
When done with the Python env, run:  
`>> deactivate`

## Usage
### Run Test Suit
`>> pytest`

### Run App
`>> flask run`

### Interacting
- Make REST requests against the API using postman, CURL, Python Requests library, etc.
- example:
    - `>> curl -XGET http://localhost/api/v1/heartbeat`
- from iPython inside the `takehome` directory while the service is running:
```python
import requests
from PyBrary import config

with open(config.TEST_USERS_FILE, 'r') as f:
    test_users = json.load(f)
with open(config.TEST_BOOKS_FILE, 'r') as f:
    test_books = json.load(f)

base_url = 'http://localhost:5000/api/v1/'

# Heartbeat
res = requests.get(base_url + 'heartbeat')
# Get all users
res = requests.get(base_url + 'users')
# Create new user
res = requests.post(base_url + 'users', json=data)
# Get user details
res = requests.get(base_url + 'users/' + test_users['RICH']['email'])
# Update user details
data['last_name'] = 'test last name'
res = requests.put(base_url + 'users/' + data['email'], json=data)
# Delete user
 res = requests.delete(base_url + 'users/' + data['email'])
# Get user wishlist
test_email = 'john@exploretheuniverse.com'
res = requests.get(base_url + 'users/' + test_email + '/wishlist')
# Add to user wishlist
data = {'isbn':  '0593395565'}
res = requests.post(base_url + 'users/' + test_email + '/wishlist', json=data)
# Remove item from user wishlist
 res = requests.delete(base_url + f"users/{test_email}/wishlist/{data['isbn']}")
# Get all books
 res = requests.get(base_url + "books")
# Create new book
 res = requests.post(base_url + "books", json=test_books['RUFF'])
# Get book detail
 res = requests.get(base_url + f"books/{test_books['RUFF']['isbn']}")
# Delete Book
 res = requests.delete(base_url + f"books/{test_books['RUFF']['isbn']}")
```

### API Description
- /api/v1/heartbeat - [GET]
    - Action: verify service is running
    - Returns: 200
- /api/v1/users - [GET]
    - Action: get all users
    - Return code: 200
    - Return data: {'STATUS': 'SUCCESS', 'DATA': {...}}
- /api/v1/users - [POST]
    - Action: create new user
    - Return code: 201
    - Return data:  {'DATA': {}, 'STATUS': 'USER CREATED'}
- /api/v1/users/\<email\> - [GET]
    - Action: get user details
    - Return code: 200
    - Return data:  {'DATA': {...}, 'STATUS': 'SUCCESS'}
- /api/v1/users/\<email\> - [PUT]
    - Action: update user details
    - Return code: 200
    - Return data: {'DATA': {}, 'STATUS': 'USER UPDATED'}
- /api/v1/users/\<email\> - [DELETE]
    - Action: get user details
    - Return code: 200
    - Return data: {'DATA': {}, 'STATUS': 'USER REMOVED'}
- /api/v1/users/\<email\>/wishlist - [GET]
    - Action: get user wishlist
    - Return code: 200
    - Return data: {'DATA': {}, 'STATUS': 'SUCCESS'}
- /api/v1/users/\<email\>/wishlist - [POST]
    - Action: add to user wishlist
    - Return code: 200
    - Return data: {'DATA': {}, 'STATUS': 'WISHLIST UPDATED'}
- /api/v1/users/\<email\>/wishlist - [DELETE]
    - Action: remove from user wishlist
    - Return code: 200
    - Return data: {'DATA': {}, 'STATUS': 'WISHLIST UPDATED'}
- /api/v1/books - [GET]
    - Action: get all books
    - Return code: 200
    - Return data: {'STATUS': 'SUCCESS', 'DATA': {...}}
- /api/v1/books - [POST]
    - Action: create new book
    - Return code: 201
    - Return data: {'STATUS': 'BOOK CREATED', 'DATA': {}}
- /api/v1/books/\<isbn\> - [GET]
    - Action: get book details
    - Return code: 200
    - Return data: {'STATUS': 'SUCCESS', 'DATA': {...}}
- /api/v1/books/\<isbn\> - [DELETE]
    - Action: remove book
    - Return code: 200
    - Return data: {'STATUS': 'BOOK REMOVED', 'DATA': {}}

## Design & Rational
[user] <-> [Flask API] <-> [db.py] <-> [TinyDB instance]

Flask
- very popular in industry for setting up REST APIs in Python
- I had a lot of familiarity with it
- by itself, not a real webserver, but plenty of tools to enable that level of functionality

TinyDB
- Very quick and easy document style database. Super fast to setup.
- Wrote the db.py in such a way that the database can later be swapped out without a requiring a code change in app.py

Config
- just used simply python file as a config. As the project grows, might swap to a tool like ConfigParser

PyTest
- Builds off of Python's standard `Unittest` library, but makes it better


## Next Steps & Features
- User login/logout circuit
- Authorization & access control
- Ability to create multiple wishlists
- Switch to more robust document based DB such as MongoDB
- Author endpoint that returns a list of all books by an author available in the PyBrary
- Input sanitization
- Exception handling
- Add logging
- Move away from using emails as identification
- integrate with true webserver like gunicorn