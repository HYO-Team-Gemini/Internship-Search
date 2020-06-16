import json
import traceback

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, HTTPException, Resource, abort, reqparse

if __name__ == "__main__":
    import job_searcher
else:
    from backend import job_searcher

app = Flask(__name__)
CORS(app)
api = Api(app, catch_all_404s=True)

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
        try:
            return job_searcher.search(args), 200
        except HTTPException as e:
            abort(e.code, message=e.description)
        except Exception as e:
            abort(500, message=f"Unexpected Server Error Occurred: {str(e)}")

##
## Actually setup the Api resource routing here
##
api.add_resource(JobList, '/jobs')


if __name__ == '__main__':
    app.run(debug=True)
