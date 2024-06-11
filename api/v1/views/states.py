#!/usr/bin/python3
"""states"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def list_states():
    """Retrieves a list of all State objects"""
    list_states = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(list_states)
