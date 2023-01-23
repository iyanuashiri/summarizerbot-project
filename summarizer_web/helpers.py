from summarizer_web.app import create_app
from summarizer_web.app.models import Summary
from summarizer_web.app import db

app = create_app()
app.app_context().push()


def create_summary(title, summary, url):
    s = Summary(title=title, summary=summary, url=url)
    db.session.add(s)
    db.session.commit()
    return s
