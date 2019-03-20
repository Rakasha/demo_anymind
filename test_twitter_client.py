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


def test_get_tweets_by_query_exceed_max_limit(fixture_client, monkeypatch):
    """ Test the scenario when the desired amount of tweets
        exceed the max_limit per Twitter-API request

        reference:
         https://developer.twitter.com/en/docs/tweets/rules-and-filtering/overview/standard-operators.html
    """
    monkeypatch.setattr(twitter_client, 'MAX_COUNT', 2)

    request_called = 0

    def mock_request(*args, **kwargs):

        nonlocal request_called
        request_called += 1

        all_tweets = [
            {'id': 1, 'text': 'text 1'},
            {'id': 2, 'text': 'text 2'},
            {'id': 3, 'text': 'text 3'},
            {'id': 4, 'text': 'text 4'},
            {'id': 5, 'text': 'text 5'},
            {'id': 6, 'text': 'text 5'},
            {'id': 7, 'text': 'text 5'}
        ]

        params = kwargs['params']
        max_id = params.get('max_id')
        count = params['count']
        if not max_id:
            return_tweets = all_tweets[-count:]
        else:
            return_tweets = all_tweets[max_id-count:max_id]

        r = requests.Response()
        r.json = lambda: {'statuses': return_tweets}
        r.status_code = 200
        return r

    client = fixture_client
    client.session.get = mock_request

    tweets = client.get_tweets_by_query(query_params=['#dummy'], limit=5)

    assert isinstance(tweets, list)
    assert len(tweets) == 5
    assert request_called == 3


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


def test_get_tweets_by_user(fixture_client):
    returned_tweets = [{'text': 'dummy tweet 1'}, {'text': 'dummy tweet 2'}]

    def mocked_session_get(*args, **kwargs):

        r = requests.Response()
        r.json = lambda: returned_tweets
        r.status_code = 200
        return r

    client = fixture_client
    client.session.get = mocked_session_get
    assert client.get_tweets_by_user('my_screen_name') == returned_tweets