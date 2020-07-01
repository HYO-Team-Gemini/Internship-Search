import json
from datetime import datetime
from pprint import pprint

import marshmallow
import pymongo
import urllib3
from bson import json_util, objectid
from flask_restful import HTTPException
from uszipcode import SearchEngine, Zipcode

if __name__ == "__main__":
    import scrape_manager
else:
    from backend import scrape_manager

credentials = json.load(open('backend/credentials.json'))
username = credentials['MongoDB']['Username']
password = credentials['MongoDB']['Password']

search_engine = SearchEngine(db_file_dir="backend/tmp")

http = urllib3.PoolManager()

def search(args: dict) -> dict:
    client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@ekko-test-qbczn.mongodb.net/jobs?retryWrites=true&w=majority")
    db = client.jobs

    search_engine = SearchEngine(db_file_dir="backend/tmp")

    results = []
    check_for_arg_issues(args)
    args = fill_missing_arguments(args)
    query_args = mongo_query_args(args)
    print(query_args)

    remaining_items = args["max_returns"]

    cursor = db.jobs.find(query_args)
    cursor.skip((args["page"] - 1) * args["max_returns"]).limit(remaining_items).sort('date', pymongo.DESCENDING)

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
    args['date'] = datetime.utcnow()
            
    db.queries.insert_one(args)
    client.close()
    return output

def check_for_arg_issues(args: dict):
    if args['zipcode'] == 0 and (args['city'] == '*' and args['state'] == '*') and args['distance'] > 0:
        raise HTTPException(description='Queried distance without specifying either zipcode or city/state pair', response=400)
    if args['max_returns'] == 0:
        raise HTTPException(description='Queried For No Returns', response=403)
    if args['max_returns'] > 100:
        raise HTTPException(description='This API will not return more than 100 entries at a time', response=403)

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
    for key in inputMongo.keys():
        item = inputMongo[key]
        if hasattr(item, 'isoformat'):
            inputMongo[key] = item.isoformat()
    
    return json.loads(json_util.dumps(inputMongo))

def build_location_query(coordinates: list, max_distance: int, min_distance: int = 0) -> dict:
    return {
        '$near': {
            '$geometry': {
                'type': 'Point',
                'coordinates': coordinates
            },
            '$maxDistance': max_distance * 1609,
            '$minDistance': min_distance * 1609
        }
    }

def fill_missing_arguments(args: dict) -> dict:
    search_engine = SearchEngine(db_file_dir="backend/tmp")
    if args['zipcode'] != 0:
        zipcode = search_engine.by_zipcode(args['zipcode'])
        location = [zipcode.lng, zipcode.lat]
        args['coordinates'] = location
        args['state'] = zipcode.state
        args['city'] = zipcode.city
    elif args['city'] != '*' and args['state'] != '*':
        zipcode = search_engine.by_city_and_state(args['city'], args['state'])[0]
        args['zipcode'] = zipcode.zipcode
        location = [zipcode.lng, zipcode.lat]
        args['coordinates'] = location
        args['state'] = zipcode.state
    return args

def get_job_by_id(id: str) -> dict:
    client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@ekko-test-qbczn.mongodb.net/jobs?retryWrites=true&w=majority")
    db = client.jobs 
    try:
        id_obj = objectid.ObjectId(id)
    except:
        raise HTTPException(description='That is invalid formatting for an ObjectID', response=400)
    job = db.jobs.find_one({"_id": id_obj})
    client.close()
    if job is None:
        raise HTTPException(description=f'No Job With ID {id} Was Found', response=200)
    return json.loads(json_util.dumps(job))

## Testing Code
if __name__ == '__main__':
    pprint(get_job_by_id('5ee6a9555d9ac3f6168baf0e'))
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
