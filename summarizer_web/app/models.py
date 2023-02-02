from datetime import datetime

from . import db


class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    summary = db.Column(db.String())
    url = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    uuid = db.Column(db.String(), unique=True)

    def __init__(self, title, summary, url, uuid):
        self.title = title
        self.summary = summary
        self.url = url
        self.uuid = uuid

    def __repr__(self):
        return f'<Summary {self.title}>'
