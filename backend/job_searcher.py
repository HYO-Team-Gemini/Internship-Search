import json
from pprint import pprint

import marshmallow
import pymongo
import urllib3
from bson import json_util
from flask_restful import HTTPException
from uszipcode import SearchEngine, Zipcode

if __name__ == "__main__":
    import scrape_manager
else:
    from backend import scrape_manager

credentials = json.load(open('backend/credentials.json'))
username = credentials['MongoDB']['Username']
password = credentials['MongoDB']['Password']
client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@ekko-test-qbczn.mongodb.net/jobs?retryWrites=true&w=majority")
db = client.jobs

search_engine = SearchEngine(db_file_dir="backend/tmp")

http = urllib3.PoolManager()

def search(args: dict) -> dict:
    search_engine = SearchEngine(db_file_dir="backend/tmp")

    results = []
    check_for_arg_issues(args)
    args = fill_missing_arguments(args)
    query_args = mongo_query_args(args)
    print(query_args)
    cursor = db.jobs.find(query_args)
    cursor.skip((args["page"] - 1) * args["max_returns"]).limit(args["max_returns"]).sort('date', pymongo.DESCENDING)

    results = list(cursor)
    jobs = {}
    for job in results:
        job = sanitize_mongo_bson(job)
        jobs[str(len(jobs.keys()) + 1)] = job
    if len(results) == 0 and args['page'] == 1 and args['zipcode'] != 0:
        results = scrape_manager.perform_query(args)
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
    if args['zipcode'] == 0 and (args['city'] == '*' and args['state'] == '*') and args['distance'] > 0:
        raise HTTPException(description='Queried distance without specifying either zipcode or city/state pair', response=400)
    if args['max_returns'] == 0:
        raise HTTPException(description='Queried For No Returns', response=403)

def mongo_query_args(args: dict) -> dict:
    query_args = {}
    for key in args.keys():
        if args[key] != '*' and (key == 'name' or key == 'employer'):
            query_args[key] = {
                "$regex": f'.*{args[key]}.*',
                "$options" :'i'
            }
    if args['distance'] != 0:
        query_args['location'] = build_location_query(args)
    return query_args

def sanitize_mongo_bson(inputMongo: dict) -> dict:
    return json.loads(json_util.dumps(inputMongo))

def build_location_query(args: dict) -> dict:
    try:
        return {
            '$geoWithin': {
                '$centerSphere': [
                    args['coordinates'], 
                    args['distance'] / 3963.2
                ]
            }
        }
    except:
        raise HTTPException(description="Issue With Distance Query", response=500)

def fill_missing_arguments(args: dict) -> dict:
    search_engine = SearchEngine(db_file_dir="backend/tmp")
    if args['zipcode'] != 0:
        zipcode = search_engine.by_zipcode(args['zipcode'])
        location = [zipcode.lng, zipcode.lat]
        args['coordinates'] = location
    elif args['city'] != '*' and args['state'] != '*':
        zipcode = search_engine.by_city_and_state(args['city'], args['state'])[0]
        args['zipcode'] = zipcode.zipcode
        location = [zipcode.lng, zipcode.lat]
        args['coordinates'] = location
    return args
    
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
