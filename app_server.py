from flask import Flask, jsonify, request, abort

import requests
import twitter_client
import settings

app = Flask(__name__)


@app.errorhandler(requests.exceptions.HTTPError)
def debug_http_error(e):
    """ For debug purpose """
    response = e.response
    return response.text, response.status_code


@app.route('/')
def root_view():
    return 'hello'

