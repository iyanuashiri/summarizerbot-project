import sys
from typing import List
import json

import tweepy
from tweepy.errors import Forbidden
from decouple import config
from slugify import slugify
from loguru import logger


logger.remove(0)
logger.add(sys.stderr, level="INFO", format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message}", serialize=False)


DOMAIN_URL = config('DOMAIN_URL')
TWITTER_CONSUMER_KEY = config("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = config("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = config("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = config("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = config("TWITTER_BEARER_TOKEN")


def connect_api(consumer_key, consumer_secret, access_token_key, access_token_secret):
    """
    Twitter Authentication Keys
    @param consumer_key:
    @param consumer_secret:
    @param access_token_key:
    @param access_token_secret:
    @return:
    """
    auth = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret,
                         access_token=access_token_key, access_token_secret=access_token_secret)
    return auth


def post_article(api, username, urls: List, replied_tweet_id, uuid):
    if len(urls) == 0:
        pass
    elif len(urls) >= 1:
        title = urls[0]['title']
        link = f'{DOMAIN_URL}/blog/{uuid}'
        reply = f'Read the summary you asked for on this link {link} below'
        result = api.create_tweet(text=f'@{username} {reply}', in_reply_to_tweet_id=replied_tweet_id)
        return result[0]['id']
    return 'Done'


def lambda_handler(event, context):
    response_payload = event['detail']['responsePayload']
    details = json.loads(response_payload)
    connected_api = connect_api(consumer_key=TWITTER_CONSUMER_KEY, consumer_secret=TWITTER_CONSUMER_SECRET,
                                access_token_secret=TWITTER_ACCESS_TOKEN_SECRET, access_token_key=TWITTER_ACCESS_TOKEN)
    tweeted_ids = []
    for detail in details:
        try:
            tweet_id = post_article(api=connected_api, username=detail['username_that_mentioned_tweet'],
                                    urls=detail['urls'], replied_tweet_id=detail['replied_tweet_id'], uuid=detail['uuid'])
            tweeted_ids.append(tweet_id)
        except Forbidden:
            logger.info("Trying to create a tweet more than once. Twitter API prevents duplicate tweets.")
    return json.dumps(tweeted_ids, default=str)
