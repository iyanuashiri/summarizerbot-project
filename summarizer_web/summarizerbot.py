from app import create_app, db
from app.models import Summary


app = create_app()


with app.app_context():
    db.create_all()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Summary': Summary}
