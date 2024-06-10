#!/usr/bin/python3
"""Creates status route"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def get_status():
    """Returns status"""
    return jsonify({"status": "OK"})


@app_views.route("/api/v1/stats")
def get_stats():
    """Returns stats"""
    from models import storage
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    classes = {
        'Amenity': storage.count(Amenity),
        'City': storage.count(City),
        'Place': storage.count(Place),
        'Review': storage.count(Review),
        'State': storage.count(State),
        'User': storage.count(User)
    }
    return jsonify(classes)
