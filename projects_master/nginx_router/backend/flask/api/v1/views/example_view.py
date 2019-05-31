#!/usr/bin/env python3
"""
Handles Getting User info.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
import json
import requests


@app_views.route(
    "/",
    methods=["GET"],
    strict_slashes=False
)
def get_root():
    return jsonify({'response': "SYNTH IS RUNNING!"})

# TODO add a post route for example json deserialization
