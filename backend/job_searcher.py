import json
from pprint import pprint

import marshmallow
import pymongo
import urllib3
from bson import json_util

credentials = json.load(open('backend/credentials.json'))
username = credentials['MongoDB']['Username']
password = credentials['MongoDB']['Password']
client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@ekko-test-qbczn.mongodb.net/jobs?retryWrites=true&w=majority")
db = client.jobs

http = urllib3.PoolManager()

def search(args: dict, remote_address: str) -> dict:
    results = []
    query_args = mongo_query_args(args)
    print(query_args)
    cursor = db.jobs.find(query_args)
    cursor.skip((args["page"] - 1) * args["max_returns"]).limit(args["max_returns"]).sort('date', pymongo.DESCENDING)

    results = list(cursor)
    jobs = {}
    for job in results:
        job = sanitize_mongo_bson(job)
        jobs[str(len(jobs.keys()) + 1)] = job
    output = { 
        "num_jobs": len(results), 
        "jobs": jobs, 
        "num_pages": int(cursor.count() / args["max_returns"]) + 1
    }
    print('Queried for:')
    pprint(args)
    return output

def check_for_arg_issues(args: dict):
    query_args = {}
    for key in args.keys():
        if args[key] != '*' and (key == 'name' or key == 'employer'):
            query_args[key] = {
                "$regex": f'.*{args[key]}.*',
                "$options" :'i'
            }
    if args['distance'] != 0:
        query_args['location'] = build_location_query(args, ip)
    return query_args

def sanitize_mongo_bson(inputMongo: dict) -> dict:
    return json.loads(json_util.dumps(inputMongo))


def build_location_query(args: dict, ip: str) -> dict:
    return {
        '$geoWithin': {
            '$centerSphere': [
                args['distance'] / 3963.2
            ]
                    args['coordinates'], 
        }
    }

## Testing Code
if __name__ == '__main__':
    pprint(search({
        'distance': 50,
        'max_returns': 50,
        'page': 1,
        'name': '*',
        'employer': '*',
        'zipcode': 0,
        'city': 'dallas',
        'state': 'texas'
    }))
