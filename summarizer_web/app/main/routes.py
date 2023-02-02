from flask import render_template, url_for


from ..models import Summary
from ..main import bp


@bp.route('/')
def index():
    # summaries = Summary.query.order_by().limit(30)
    # summaries = Summary.query.limit(15).all()
    summaries = Summary.query.all()[-15:]
    title = "This is the future"
    return render_template('index.html', title=title, summaries=summaries)


@bp.route('/blog/<string:uuid>')
def detail(uuid):
    summary = Summary.query.filter_by(uuid=uuid).first()
    return render_template('detail.html', summary=summary)


# @bp.route('/blog/<int:summarizer_id>')
# def detail(summarizer_id):
#     summary = Summary.query.get(summarizer_id)
#     return render_template('detail.html', summary=summary)
