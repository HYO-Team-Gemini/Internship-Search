import json
import traceback
from datetime import datetime

import pymongo
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, HTTPException, Resource, abort, reqparse

if __name__ == "__main__":
    import job_searcher
else:
    from backend import job_searcher

credentials = json.load(open('backend/credentials.json'))
username = credentials['MongoDB']['Username']
password = credentials['MongoDB']['Password']

app = Flask(__name__)
CORS(app)
api = Api(app, catch_all_404s=True)

joblist_parser = reqparse.RequestParser()
joblist_parser.add_argument('name', default='*', type=str)
joblist_parser.add_argument('employer', default='*', type=str)
joblist_parser.add_argument('distance', default=0, type=int)
joblist_parser.add_argument('page', default=1, type=int)
joblist_parser.add_argument('max_returns', default=50, type=int)
joblist_parser.add_argument('zipcode', default=0, type=int)
joblist_parser.add_argument('city', default='*', type=str)
joblist_parser.add_argument('state', default='*', type=str)

# JobList
# shows a list of all jobs
class JobList(Resource):
    def get(self):
        args = joblist_parser.parse_args()
        try:
            return job_searcher.search(args), 200
        except HTTPException as e:
            abort(e.code, message=e.description)
        except Exception as e:
            log_error(e, args)
            abort(500, message=f"Unexpected Server Error Occurred: {str(e)}")

def log_error(error: Exception, args: dict={}):
    client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@ekko-test-qbczn.mongodb.net/jobs?retryWrites=true&w=majority")
    client.errors.log.insert_one({'error': str(error), 'args': args, 'date': datetime.utcnow()})
    client.close()

##
## Actually setup the Api resource routing here
##
api.add_resource(JobList, '/jobs')


if __name__ == '__main__':
    app.run(debug=True)
