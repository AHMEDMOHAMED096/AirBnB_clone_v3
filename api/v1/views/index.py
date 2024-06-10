#!/usr/bin/python3
"""Creates status route"""
from api.v1.views import app_views


@app_views.route("/status")
def get_status():
    """Returns status"""
    return {"status": "OK"}
