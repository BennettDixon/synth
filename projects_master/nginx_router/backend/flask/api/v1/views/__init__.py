#!/usr/bin/python3
"""init file for views in REST API
   adds prefix of /api/v1 too all routes registered with the blueprint
"""
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.example_view import *
