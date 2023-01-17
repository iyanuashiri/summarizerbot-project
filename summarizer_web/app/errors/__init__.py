from flask import Blueprint

bp = Blueprint('errors', __name__)

from summarizer_web.app.errors import handlers
