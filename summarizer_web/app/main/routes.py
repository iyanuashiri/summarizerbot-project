from flask import render_template


from ..models import Summary
from ..main import bp


@bp.route('/')
def index():
    # summaries = Summary.query.order_by().limit(30)
    # summaries = Summary.query.limit(15).all()
    summaries = Summary.query.all()[-15:-1]
    title = "This is the future"
    return render_template('index.html', title=title, summaries=summaries)


@bp.route('/blog/<int:summary_id>')
def detail(summary_id):
    summary = Summary.query.get(summary_id)
    return render_template('detail.html', summary=summary)
