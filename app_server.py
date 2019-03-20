import requests
from flask import Flask, jsonify, request, g

import twitter_client
import settings

app = Flask(__name__)

DEFAULT_REQUEST_LIMIT = 30


def get_client():
    if not hasattr(g, 'twitter_client'):
        c = twitter_client.Client(settings.API_KEY, settings.API_SECRET_KEY)
        c.auth()
        g.twitter_client = c
    return g.twitter_client


@app.route('/')
def root_view():
    return 'hello'


@app.route('/hashtags/<string:hashtag>', methods=['GET'])
def get_by_hash_tag(hashtag):
    limit = int(request.args.get('limit', DEFAULT_REQUEST_LIMIT))

    client = get_client()
    tweets = client.get_tweets_by_hashtag(hashtag, limit=limit)
    if not tweets:
        return jsonify(message="No tweet found"), 404

    formatted_tweets = list(map(twitter_client.format_tweet, tweets))
    return jsonify(formatted_tweets)


@app.route('/users/<string:screen_name>', methods=['GET'])
def get_by_user(screen_name):
    limit = int(request.args.get('limit', DEFAULT_REQUEST_LIMIT))

    client = get_client()
    tweets = client.get_tweets_by_user(screen_name, limit=limit)
    if not tweets:
        return jsonify(message="No tweet found"), 404

    formatted_tweets = list(map(twitter_client.format_tweet, tweets))
    return jsonify(formatted_tweets)
