import pytest

import requests
from unittest.mock import Mock

import twitter_client

EXAMPLE_TWEET = {
        "created_at": "Tue Mar 05 23:50:44 +0000 2019",
        "id": 1103080434630443009,
        "id_str": "1103080434630443009",
        "text": "It’s an incredible time to become a Data Engineer! Our @udacity School of #DataScience just launched the Data Engin… https://t.co/mYRr5mmGHB",
        "truncated": True,
        "entities": {
            "hashtags": [
                {
                    "text": "DataScience",
                    "indices": [
                        74,
                        86
                    ]
                }
            ],
            "symbols": [],
            "user_mentions": [
                {
                    "screen_name": "udacity",
                    "name": "Udacity",
                    "id": 326912209,
                    "id_str": "326912209",
                    "indices": [
                        55,
                        63
                    ]
                }
            ],
            "urls": [
                {
                    "url": "https://t.co/mYRr5mmGHB",
                    "expanded_url": "https://twitter.com/i/web/status/1103080434630443009",
                    "display_url": "twitter.com/i/web/status/1…",
                    "indices": [
                        117,
                        140
                    ]
                }
            ]
        },
        "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
        "in_reply_to_status_id": None,
        "in_reply_to_status_id_str": None,
        "in_reply_to_user_id": None,
        "in_reply_to_user_id_str": None,
        "in_reply_to_screen_name": None,
        "user": {
            "id": 318063815,
            "id_str": "318063815",
            "name": "Sebastian Thrun",
            "screen_name": "SebastianThrun",
            "location": "Mountain View, CA",
            "description": "Founder, President Udacity.",
            "url": "https://t.co/rlrjbh9s51",
            "entities": {
                "url": {
                    "urls": [
                        {
                            "url": "https://t.co/rlrjbh9s51",
                            "expanded_url": "http://udacity.com",
                            "display_url": "udacity.com",
                            "indices": [
                                0,
                                23
                            ]
                        }
                    ]
                },
                "description": {
                    "urls": []
                }
            },
            "protected": False,
            "followers_count": 68408,
            "friends_count": 8,
            "listed_count": 2096,
            "created_at": "Wed Jun 15 22:24:13 +0000 2011",
            "favourites_count": 30,
            "utc_offset": None,
            "time_zone": None,
            "geo_enabled": False,
            "verified": False,
            "statuses_count": 676,
            "lang": "en",
            "contributors_enabled": False,
            "is_translator": False,
            "is_translation_enabled": False,
            "profile_background_color": "C0DEED",
            "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
            "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
            "profile_background_tile": False,
            "profile_image_url": "http://pbs.twimg.com/profile_images/459372432806014977/ftbXtMDO_normal.png",
            "profile_image_url_https": "https://pbs.twimg.com/profile_images/459372432806014977/ftbXtMDO_normal.png",
            "profile_banner_url": "https://pbs.twimg.com/profile_banners/318063815/1505968489",
            "profile_link_color": "1DA1F2",
            "profile_sidebar_border_color": "C0DEED",
            "profile_sidebar_fill_color": "DDEEF6",
            "profile_text_color": "333333",
            "profile_use_background_image": True,
            "has_extended_profile": False,
            "default_profile": True,
            "default_profile_image": False,
            "following": None,
            "follow_request_sent": None,
            "notifications": None,
            "translator_type": "none"
        },
        "geo": None,
        "coordinates": None,
        "place": None,
        "contributors": None,
        "is_quote_status": False,
        "retweet_count": 26,
        "favorite_count": 149,
        "favorited": False,
        "retweeted": False,
        "possibly_sensitive": False,
        "lang": "en"
    }


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


def test_format_tweet():

    correct_result = {"account": {"fullname": "Sebastian Thrun",
                                  "href": "/SebastianThrun",
                                  "id": 318063815},
                      "date": "11:50 PM - 5 Mar 2019",
                      "hashtags": ["#DataScience"],
                      "likes": 149,
                      "retweets": 26,
                      "text": "It’s an incredible time to become a Data Engineer! Our @udacity School of #DataScience just launched the Data Engin… https://t.co/mYRr5mmGHB"}

    result = twitter_client.format_tweet(EXAMPLE_TWEET)
    assert result == correct_result

def test_format_tweet_date():
    source_string = 'Tue Mar 05 23:50:44 +0000 2019'
    correct_answer = '11:50 PM - 5 Mar 2019'
    result =  twitter_client.format_tweet_date(source_string)
    assert result == correct_answer