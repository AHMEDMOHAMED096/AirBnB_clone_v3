#!/usr/bin/python3
"""starts a Flask web application"""
import os
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def close_session(exception=None):
    """Closes session"""
    from models import storage

    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handles 404 error and gives json formatted response"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
