import pytest

import requests
from unittest.mock import Mock

import twitter_client


@pytest.fixture
def fixture_client():
    api_key = 'xxxx'
    api_secret_key = 'xxxx'
    return twitter_client.Client(api_key, api_secret_key)


def test_auth(fixture_client):
    client = fixture_client
    my_token = 'my_oauth2_token'
    def mocked_get_oauth2_token(*args, **kwargs):
        return my_token

    client.get_oauth2_token = mocked_get_oauth2_token
    client.auth()
    assert client.auth_token == my_token
    print(client.session.headers)
    assert client.session.headers['Authorization'] == 'Bearer {}'.format(my_token)


def test_set_auth_token(fixture_client):
    client = fixture_client
    my_token = 'xxxTokenxxx'
    client.auth_token = my_token

    assert client.session.headers['Authorization'] == 'Bearer {}'.format(my_token)
    assert client.auth_token == my_token


def test_get_tweets_by_query(fixture_client):

    def mockrequest(*args, **kwargs):

        r = requests.Response()
        tweets = [{'text': 'dummy tweet 1'}, {'text': 'dummy tweet 2'}]
        r.json = lambda: {'statuses': tweets}
        r.status_code = 200
        return r

    client = fixture_client
    client.session.get = mockrequest
    tweets = client.get_tweets_by_query(query_params=['#dummy'], limit=3)
    assert isinstance(tweets, list)


def test_get_tweets_by_hashtag(fixture_client):

    client = fixture_client
    correct_values = [{'text': 'dummy tweet 1'}, {'text': 'dummy tweet 2'}]
    correct_limit = 123
    hash_tag = 'dummy'

    mocked_get_tweets_by_query = Mock(return_value=correct_values)

    client.get_tweets_by_query = mocked_get_tweets_by_query
    tweets = client.get_tweets_by_hashtag('dummy', limit=correct_limit)

    assert tweets == correct_values
    mocked_get_tweets_by_query.assert_called_with(query_params=['#'+hash_tag],
                                                  limit=correct_limit)