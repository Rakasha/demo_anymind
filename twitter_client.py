import requests
import functools


API_HOST = 'https://api.twitter.com'
DEFAULT_API_VERSION = '1.1'


class Client(object):

    def __init__(self, api_key, api_secret_key, api_version=DEFAULT_API_VERSION, api_host=API_HOST):
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.base_url = '{}/{}'.format(api_host, api_version)
        self.base_auth_url = api_host

        self._auth_token = None
        self.session = requests.Session()

    def auth(self):
        new_token = self.get_oauth2_token(self.api_key, self.api_secret_key)
        self._auth_token = new_token
        self._set_auth_header(new_token)

    def _set_auth_header(self, auth_token):
        self.session.headers['Authorization'] = 'Bearer {}'.format(auth_token)

    @property
    def auth_token(self):
        return self._auth_token

    @auth_token.setter
    def auth_token(self, new_auth_token):
        self._auth_token = new_auth_token
        self._set_auth_header(new_auth_token)

    def get_oauth2_token(self, api_key, api_secret_key):
        url = self.base_auth_url + '/oauth2/token'
        r = self.session.post(url,
                              auth=(api_key, api_secret_key),
                              data={'grant_type': 'client_credentials'})
        r.raise_for_status()
        return r.json()['access_token']


    def get_tweets_by_query(self, query_params, limit=30):
        """ Fetch tweets by given list of query conditions.

        For building query operators see:
         https://developer.twitter.com/en/docs/tweets/rules-and-filtering/overview/standard-operators.html

        :param query_params: list of string
        :param limit: number of tweets to fetch
        :return: list of dict, each represents a tweet
        """

        url = self.base_url + '/search/tweets.json'
        q_string = ' '.join(query_params)
        r = self.session.get(url, params={'q': q_string})

        r.raise_for_status()
        tweets = r.json()['statuses']
        return tweets
