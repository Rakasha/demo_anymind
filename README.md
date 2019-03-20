#demo_anymind
 
RESTful-API server for searching Tweet data


# Requirements
- flask
- requests
- pytest

# Installation

`git clone https://github.com/Rakasha/demo_anymind.git`

`cd` into project dir

`pip install -r requirements.txt` (recommand to use [virtualenv](https://docs.python.org/3.6/library/venv.html))

# Setup API server

## Server Configurations


1.**Register Twitter developer account and generate the API key**

The server relies on Twitter API for searching Tweets.
So you'll need to register a Twitter developer account and generate the api keys first

2.**Configure server settings**

Create a file `settings.py` under the project root that contains the following key-value pairs. Check the `settings.py.exmaple` for an example usage.

```python
API_KEY = 'your twitter api key'
API_SECRET_KEY = 'your twitter api secret key'
```
3.**Spin-up the api-server**

 Run the following commands:

```bash
export FLASK_APP=app_server.py
python -m flask run --host=<your host> --port=<your port num>
```

# Usage

## RESTful API endpoints
### Get tweets by hashtag 
Get a list of tweets that contain the given hashtag

URL: `/hashtags/<hashtag>`

Query params: 

- `limit`: (Optional) number of tweets to return

Example:

```bash
curl -X GET \
  'http://localhost:5000/hashtags/udacity?limit=2' \
  -H 'Content-Type: application/json'
```

Returns:

```json
[
    {
        "account": {
            "fullname": "tempmedia",
            "href": "/tempmedia1",
            "id": 1082364930412765186
        },
        "date": "03:17 PM - 20 Mar 2019",
        "hashtags": [
            "#javascript",
            "#coding",
            "#hacking",
            "#programmer"
        ],
        "likes": 0,
        "retweets": 4,
        "text": "RT @dr_vitus_zato: How to be a successful freelancer in any career =&gt;  https://t.co/lCb7rM3cTC #javascript #coding #hacking #programmer #we…"
    },
    {
        "account": {
            "fullname": "Aaron Cuddeback",
            "href": "/AaronCuddeback",
            "id": 310897418
        },
        "date": "03:16 PM - 20 Mar 2019",
        "hashtags": [
            "#javascript",
            "#coding",
            "#hacking",
            "#programmer"
        ],
        "likes": 0,
        "retweets": 4,
        "text": "RT @dr_vitus_zato: How to be a successful freelancer in any career =&gt;  https://t.co/lCb7rM3cTC #javascript #coding #hacking #programmer #we…"
    }
]
```


### Get tweets by name
Get a list of tweets from the given user using his/her `screen name`

URL: `/users/<screen_name>`

Query params:

- `limit`: (Optional) number of tweets to return

Example:

```bash
curl -X GET \
  'http://localhost:5000/users/SebastianThrun?limit=15' \
  -H 'Content-Type: application/json'
```

Returns:

```json
[
  {
    "account": {
      "fullname": "Sebastian Thrun",
      "href": "/SebastianThrun",
      "id": 318063815
    },
    "date": "04:07 AM - 20 Mar 2019",
    "hashtags": [],
    "likes": 71,
    "retweets": 11,
    "text": "I am very excited to announce a NEW Nanodegree Program: Programming for Data Science with R. This course is designe\u2026 https://t.co/CPoaZiaeom"
  },
  {
    "account": {
      "fullname": "Sebastian Thrun",
      "href": "/SebastianThrun",
      ...
```

# Testing
Simply run `pytest` under the project root:

```bash
$ pytest .
```

