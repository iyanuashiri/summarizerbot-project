from flask import Blueprint

bp = Blueprint('main', __name__)

from summarizer_web.app.main import routes