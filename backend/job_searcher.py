import json
from pprint import pprint

import marshmallow
import pymongo
from bson import json_util

credentials = json.load(open('backend/credentials.json'))
username = credentials['MongoDB']['Username']
password = credentials['MongoDB']['Password']
client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@ekko-test-qbczn.mongodb.net/jobs?retryWrites=true&w=majority")
db = client.jobs

def search(args: dict) -> dict:
    query_args = mongo_query_args(args)
    filtered_jobs = list(db.jobs.find(query_args))
    jobs = {}
    for job in filtered_jobs:
        job = json.loads(json_util.dumps(job))
        jobs[str(len(jobs.keys()) + 1)] = job
    output = { "num_jobs": len(filtered_jobs), "jobs": jobs}
    pprint('Queried for: ')
    pprint(args)
    pprint(output)
    return output

def mongo_query_args(args: dict) -> dict:
    query_args = {}
    for key in args.keys():
        if args[key] != '*':
            query_args[key] = {
                "$regex": f'.*{args[key]}.*',
                "$options" :'i'
            }
    return query_args
