from flask import Flask, jsonify, request

import twitter_client
import settings

app = Flask(__name__)

DEFAULT_REQUEST_LIMIT = 30


@app.route('/')
def root_view():
    return 'hello'


@app.route('/hashtags/<string:hashtag>')
def get_by_hash_tag(hashtag):
    limit = request.args.get('limit', DEFAULT_REQUEST_LIMIT)
    client = twitter_client.Client(settings.API_KEY, settings.API_SECRET_KEY)
    client.auth()

    tweets = client.get_tweets_by_hashtag(hashtag, limit=limit)
    if not tweets:
        return jsonify(message="No tweet found"), 404
    return jsonify(tweets)


@app.route('/users/<string:screen_name>')
def get_by_user(screen_name):
    limit = request.args.get('limit', DEFAULT_REQUEST_LIMIT)
    client = twitter_client.Client(settings.API_KEY, settings.API_SECRET_KEY)
    client.auth()

    tweets = client.get_tweets_by_user(screen_name, limit=limit)
    if not tweets:
        return jsonify(message="No tweet found"), 404
    return jsonify(tweets)