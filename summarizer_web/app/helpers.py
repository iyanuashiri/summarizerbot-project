from . import create_app, db
from . import models


app = create_app()
app.app_context().push()


def create_summary(title, summary, url):
    s = models.Summary(title=title, summary=summary, url=url)
    db.session.add(s)
    db.session.commit()
    return s
