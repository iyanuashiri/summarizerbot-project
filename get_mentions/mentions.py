import logging
from operator import itemgetter

import tweepy
from get_mentions.config import redis_db, TWITTER_USERNAME_ID, TWITTER_BEARER_TOKEN

logger = logging.getLogger()


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


def process_urls(urls):
    for url in urls:
        url, expanded_url = url['url'], url['expanded_url']


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
    since_id = int(redis_db.get('since_id'))
    connected_api = connect_api(bearer_token=TWITTER_BEARER_TOKEN)
    details = list(get_latest_mentions(api=connected_api, user_id=TWITTER_USERNAME_ID, since_id=since_id))
    sorted_details = sorted(details, key=itemgetter('newest_id'), reverse=True)
    redis_db.set('since_id', sorted_details[0]['newest_id'])
    return details
