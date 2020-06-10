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
    query_args = mongo_query_args(args, remote_address)
    results = list(db.jobs.find(query_args))
    jobs = {}
    for job in results:
        job = sanitize_mongo_bson(job)
        jobs[str(len(jobs.keys()) + 1)] = job
    output = { "num_jobs": len(results), "jobs": jobs}
    print('Queried for:')
    pprint(args)
    pprint(output)
    return output

def mongo_query_args(args: dict, ip: str) -> dict:
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

def get_user_coordinates(ip: str) -> list:
    api_key = credentials["IPStack"]["Access Key"]
    api_address = f"http://api.ipstack.com/{ip}?access_key={api_key}"
    result = json.loads(http.request('GET', api_address).data)
    return [result['latitude'], result['longitude']]

def build_location_query(args: dict, ip: str) -> dict:
    return { 
        '$near' : {
            '$geometry': { 
                'type': "Point",
                'coordinates': get_user_coordinates(ip) 
            },
            '$minDistance': 0,
            '$maxDistance': 1609.34 * args['distance']
        }
    }
    

search({'distance': 5, 'max_returns': 50}, '73.245.3.190')