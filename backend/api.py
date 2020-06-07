from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import json
import job_searcher

app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('name', default='*', type=str)
parser.add_argument('employer', default='*', type=str)
parser.add_argument('post_age', default='*', type=int)
parser.add_argument('distance', default='*', type=int)

# JobList
# shows a list of all jobs
class JobList(Resource):
    def get(self):
        args = parser.parse_args()
        output = job_searcher.search(args)
        return output

##
## Actually setup the Api resource routing here
##
api.add_resource(JobList, '/jobs')


if __name__ == '__main__':
    app.run(debug=True)
