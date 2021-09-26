from flask import Flask

app = Flask(__name__)

@app.route("/heartbeat")
def heartbeat():
    return { "status": "OK" }