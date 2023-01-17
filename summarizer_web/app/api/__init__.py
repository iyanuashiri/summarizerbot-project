from flask import Blueprint

bp = Blueprint('resources', __name__)

from summarizer_web.app.api import resources