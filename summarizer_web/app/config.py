from dataclasses import dataclass
import os

basedir = os.path.abspath(os.path.dirname(__file__))


@dataclass
class Config:
    DEBUG: bool = True
    TESTING: bool = False
    CSRF_ENABLED: bool = True
    SECRET_KEY: str = 'my-secret-key'
    # SECRET_KEY: str = os.getenv('SECRET_KEY')
    # LOG_TO_STDOUT: str = os.getenv('LOG_TO_STDOUT')
    SQLALCHEMY_DATABASE_URI: str = 'postgres://iyanuashiri:PnJ90QfsBGwc@ep-crimson-pond-299050.us-east-2.aws.neon.tech/neondb'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    TEMPLATES_AUTO_RELOAD: bool = True


# or 'sqlite:///' + os.path.join(basedir, '../app.db')