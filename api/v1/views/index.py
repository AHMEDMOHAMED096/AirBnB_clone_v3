#!/usr/bin/python3
"""Creates status route"""
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def get_status():
    """Returns status"""
    return {"status": "OK"}


@app_views.route("/api/v1/stats")
def get_stats():
    """Returns stats"""
    return storage.count()
