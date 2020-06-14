from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import json
from backend import job_searcher

app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('name', default='*', type=str)
parser.add_argument('employer', default='*', type=str)
parser.add_argument('distance', default=0, type=int)
parser.add_argument('page', default=1, type=int)
parser.add_argument('max_returns', default=50, type=int)
parser.add_argument('zipcode', default=0, type=int)
parser.add_argument('city', default='*', type=str)
parser.add_argument('state', default='*', type=str)

# JobList
# shows a list of all jobs
class JobList(Resource):
    def get(self):
        args = parser.parse_args()
        user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            output = job_searcher.search(args, user_ip)
        except:
            output = {'message': 'Error Occurred Somewhere'}
        return output

##
## Actually setup the Api resource routing here
##
api.add_resource(JobList, '/jobs')


if __name__ == '__main__':
    app.run(debug=True)
