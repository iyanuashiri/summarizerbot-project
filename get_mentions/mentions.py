import logging
import json

import tweepy
import redis
from decouple import config
# from get_mentions.config import redis_db, TWITTER_USERNAME_ID, TWITTER_BEARER_TOKEN, SINCE_ID

logger = logging.getLogger()


TWITTER_CONSUMER_KEY = config("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = config("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = config("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = config("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_USERNAME = config("TWITTER_USERNAME")
TWITTER_USERNAME_ID = config("TWITTER_USERNAME_ID")
TWITTER_BEARER_TOKEN = config("TWITTER_BEARER_TOKEN")

SINCE_ID = config("SINCE_ID")

# REDIS_URL = config('REDIS_URL')

REDIS_PASSWORD_DEV = config('REDIS_PASSWORD_DEV')
REDIS_PORT_DEV = config('REDIS_PORT_DEV')
REDIS_HOST_DEV = config('REDIS_HOST_DEV')

REDIS_PASSWORD_PROD = config('REDIS_PASSWORD_DEV')
REDIS_PORT_PROD = config('REDIS_PORT_DEV')
REDIS_HOST_PROD = config('REDIS_HOST_DEV')


if config("CURRENT_ENV") == "development":
    redis_db = redis.Redis(host=REDIS_HOST_DEV, port=REDIS_PORT_DEV, password=REDIS_PASSWORD_DEV, ssl=True)
elif config("CURRENT_ENV") == "production":
    redis_db = redis.Redis(host=REDIS_HOST_PROD, port=REDIS_PORT_PROD, password=REDIS_PASSWORD_PROD, ssl=True)
    # redis_url = config("REDIS_URL")
    # redis_db = redis.from_url(redis_url)


def connect_api(bearer_token):
    """
    Twitter Bearer Token
    :param bearer_token:
    @return:
    """
    auth = tweepy.Client(bearer_token=bearer_token)
    return auth


def process_referenced_tweets(referenced_tweets):
    try:
        for referenced_tweet in referenced_tweets:
            if referenced_tweet['type'] == 'replied_to':
                referenced_tweet_id = referenced_tweet['id']

                return referenced_tweet_id, referenced_tweet['type']
            else:
                return '1612594344501837824' 'check'
    except TypeError:
        return '1612594344501837824', 'check'


def get_latest_mentions(api, user_id, since_id):
    response = api.get_users_mentions(id=user_id, since_id=since_id,
                                      tweet_fields=['referenced_tweets', 'author_id'])
    meta = response[3]
    newest_id = meta['newest_id']
    mentioned_tweets = response[0]
    for mentioned_tweet in mentioned_tweets:
        referenced_tweets = mentioned_tweet['referenced_tweets']

        replied_tweet_id, reference_tweet_type = process_referenced_tweets(referenced_tweets=referenced_tweets)

        response_2 = api.get_tweet(id=replied_tweet_id, tweet_fields=['entities', 'author_id', 'text'])
        response_2_data = response_2[0]['data']
        entities = response_2_data['entities']
        try:
            urls = entities['urls']
        except KeyError:
            urls = []

        user_id_that_mentioned_tweet = mentioned_tweet['author_id']
        response_3 = api.get_user(id=mentioned_tweet['author_id'])
        username_that_mentioned_tweet = response_3[0]['data']['username']

        yield {'urls': urls, 'replied_tweet_id': replied_tweet_id, 'replied_tweet': response_2_data['text'],
               'mentioned_tweet_id': mentioned_tweet['id'], 'mentioned_tweet': mentioned_tweet['text'],
               'user_id_that_mentioned_tweet': user_id_that_mentioned_tweet,
               'username_that_mentioned_tweet': username_that_mentioned_tweet,
               'username_that_mentioned_bot': mentioned_tweet, 'username_that_shared_link': '',
               'newest_id': newest_id, 'entities': entities, 'response_2': response_2,
               'response_2_data': response_2_data, 'reference_tweet_type': reference_tweet_type}


def lambda_handler(event, context):
    event = event
    if redis_db.get('since_id') is None:
        since_id = SINCE_ID
    else:
        since_id = redis_db.get('since_id')

    connected_api = connect_api(bearer_token=TWITTER_BEARER_TOKEN)
    details = list(get_latest_mentions(api=connected_api, user_id=TWITTER_USERNAME_ID, since_id=since_id))
    redis_db.set('since_id', details[0]['newest_id'])
    return json.dumps(details, default=str)
