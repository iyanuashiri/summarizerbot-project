from flask_restful import Resource, reqparse, marshal_with, fields, Api

from . import bp
from ..helpers import create_summary

api = Api(bp)


summary_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'summary': fields.String,
    'url': fields.String,
    'uuid': fields.String,
}


class SummaryListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', dest='title', location='form', required=True)
        self.reqparse.add_argument('summary', dest='summary', location='form', required=True,
                                   help='the summary of the article')
        self.reqparse.add_argument('url', dest='url', location='form', required=True, help='the url of the article')
        self.reqparse.add_argument('uuid', dest='uuid', location='form', required=True)
        super(SummaryListAPI, self).__init__()

    @marshal_with(summary_fields)
    def post(self):
        args = self.reqparse.parse_args()
        summary = create_summary(title=args['title'], summary=args['summary'], url=args['url'], uuid=args['uuid'])
        return summary


api.add_resource(SummaryListAPI, '/create')
