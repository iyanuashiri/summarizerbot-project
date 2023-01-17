from dataclasses import dataclass
import os

from decouple import config

# import redis

basedir = os.path.abspath(os.path.dirname(__file__))


@dataclass
class Config:
    DEBUG: bool = False
    TESTING: bool = False
    CSRF_ENABLED: bool = True
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    LOG_TO_STDOUT: str = os.getenv('LOG_TO_STDOUT')
    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    TEMPLATES_AUTO_RELOAD: bool = True


SINCE_ID = config("SINCE_ID")
