from . import create_app, db
from . import models


app = create_app()
app.app_context().push()


def create_summary(title, summary, url, uuid):
    s = models.Summary(title=title, summary=summary, url=url, uuid=uuid)
    db.session.add(s)
    db.session.commit()
    return s
