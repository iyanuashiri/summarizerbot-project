from datetime import datetime

from summarizer_web.app import db


class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    summary = db.Column(db.String())
    url = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, title, summary, url):
        self.title = title
        self.summary = summary
        self.url = url

    def __repr__(self):
        return f'<Summary {self.title}>'
