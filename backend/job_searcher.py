import marshmallow
import json
from pprint import pprint
import pymongo

credentials = json.load(open('backend/credentials.json'))
username = credentials['MongoDB']['Username']
password = credentials['MongoDB']['Password']
client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@ekko-test-qbczn.mongodb.net/jobs?retryWrites=true&w=majority")
db = client.test
serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)
def search(args: dict) -> dict:
    jobs = {}
    filtered_jobs = {}
    for key in jobs:
        job = jobs[key]
        if args['name'] == '*' or args['name'] in job['name']:
            if args['employer'] == '*' or args['employer'] in job['employer']:
                job_id = len(filtered_jobs.keys()) + 1
                filtered_jobs[str(job_id)] = job
    output = { "num_jobs": len(filtered_jobs.keys()), "jobs": filtered_jobs}
    return output

## print(search({'name': '*', 'employer': '*'}))