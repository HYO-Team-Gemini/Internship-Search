from flask import Flask
from flask_restful import Api, Resource
import json

app = Flask(__name__)
api = Api(app)

jobs = json.load(open('example-models/jobs.json'))

# JobList
# shows a list of all jobs
class JobList(Resource):
    def get(self):
        return jobs

##
## Actually setup the Api resource routing here
##
api.add_resource(JobList, '/jobs')


if __name__ == '__main__':
    app.run(debug=True)
