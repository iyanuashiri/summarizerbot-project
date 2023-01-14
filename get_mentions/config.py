import redis
from decouple import config

# DOMAIN_URL = config('DOMAIN_URL')

TWITTER_CONSUMER_KEY = config("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = config("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = config("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = config("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_USERNAME = config("TWITTER_USERNAME")
TWITTER_USERNAME_ID = config("TWITTER_USERNAME_ID")
TWITTER_BEARER_TOKEN = config("TWITTER_BEARER_TOKEN")

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

