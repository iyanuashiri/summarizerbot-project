import logging

from twitter_threader import connect_api, threader
from goose3 import Goose

from summarizer_web.config import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_CONSUMER_SECRET, \
    TWITTER_CONSUMER_KEY, DOMAIN_URL, redis_db
from summarizer_web.app import create_app
from summarizer_web.app.models import Summary
from summarizer_web.app import db
from summarizer_bot.summarize import summarize_article

app = create_app()
app.app_context().push()

logger = logging.getLogger()

api = connect_api(consumer_key=TWITTER_CONSUMER_KEY, consumer_secret=TWITTER_CONSUMER_SECRET,
                  access_token_key=TWITTER_ACCESS_TOKEN, access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)


def post_article(screen_name, url, sentences_count, in_reply_to_status_id):
    username = screen_name
    threaded = threader.Thread(api=api)
    summary = summarize_article(url=url, sentence_count=sentences_count)
    title = get_title(url)
    s = Summary(title=title, summary=summary, url=url)
    db.session.add(s)
    db.session.commit()
    reply = f'Read the summary you asked for on this link {DOMAIN_URL}/blog/{s.id} below'
    # thread = threaded.post_thread(reply, f'@{username}', in_reply_to_status_id)
    # thread = api.update_status(f'@{username} {reply}', in_reply_to_status_id)

    thread = api.update_status(f'@{username} {reply}', in_reply_to_status_id=in_reply_to_status_id)

    return {'message': f'@{username} {reply}'}


def get_latest_mentions(api, since_id):
    latest_id = int(since_id)

    mention_tweets = api.mentions_timeline(since_id=since_id)
    for tweet in mention_tweets:
        redis_db.set('since_id', latest_id)
        latest_id = max(tweet.id, since_id)

        hashtags, in_reply_to_status_id, screen_name = tweet.entities[
            "hashtags"], tweet.in_reply_to_status_id, tweet.user.screen_name

        sentence_count = 5

        text = ''
        try:
            text = str(hashtags[0]['text'])
        except IndexError:
            pass

        # get original tweet
        status = api.get_status(in_reply_to_status_id, tweet_mode='extended')
        # status_id = status.id

        url = ''
        try:
            urls = status.entities["urls"]
            url = urls[0]["expanded_url"]
        except IndexError:
            pass

        post_article(screen_name, url, sentence_count, in_reply_to_status_id)

    return latest_id


def get_title(url):
    g = Goose()
    article = g.extract(url=url)
    title = article.title
    return title


event = {'since_id': '', 'api': ''}


def lambda_handler(event, context):
    event = event
    since_id = int(redis_db.get('since_id'))

    latest_id = get_latest_mentions(api=api, since_id=since_id)
    redis_db.set('since_id', latest_id)
    return latest_id, event
