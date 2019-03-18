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


@app.route('/hashtags/<string:hashtag>')
def get_by_hash_tag(hashtag):
    limit = request.args.get('limit')
    client = twitter_client.Client(settings.API_KEY, settings.API_SECRET_KEY)
    client.auth()

    tweets = client.get_tweets_by_hashtag(hashtag, limit=limit)
    if not tweets:
        abort(404)
    return jsonify(tweets)

