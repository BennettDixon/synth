#!/usr/bin/python3
"""main app file for Flask instance in REST API
"""
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from api.v1.views import app_views
import os
from flask import Flask, redirect, url_for


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(exc=None):
    """called on teardown of app contexts of flask
    """
    pass


def page_not_found(error):
    """ custom 404 error response page
    """
    return jsonify({'error': "Not found"}), 404


@app.route('/', strict_slashes=False)
def hello_world():
    """ basic route to return some json
    """
    return jsonify(api_goes="here!")


if __name__ == "__main__":
    """run the app if the script is not being imported
    """
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.register_error_handler(404, page_not_found)

    # pulled as environmental variables
    fetched_host = os.environ.get('YOUR_HOST_VAR')
    fetched_port = os.environ.get('YOUR_PORT_VAR')
    # DEFAULTS FOR HOST AND PORT
    if fetched_host is None:
        fetched_host = '0.0.0.0'
    if fetched_port is None:
        fetched_port = 5005
    app.run(host=fetched_host, port=fetched_port, threaded=True)
