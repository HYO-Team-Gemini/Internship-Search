import json
from pprint import pprint

import pymongo
from uszipcode import SearchEngine, Zipcode

from backend import extras, glassdoor, linkedin

credentials = json.load(open('backend/credentials.json'))
username = credentials['MongoDB']['Username']
password = credentials['MongoDB']['Password']
client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@ekko-test-qbczn.mongodb.net/jobs?retryWrites=true&w=majority")
db = client.jobs
search = SearchEngine(db_file_dir="backend/tmp")

def scrape_for_jobs(name: str, coordinates: list) -> list:
    lon = coordinates[0]
    lat = coordinates[1]
    zipcode = search.by_coordinates(lat, lon)[0].zipcode
    return scrape_for_jobs(name, zipcode)

def scrape_for_jobs(name: str, zipcode: str) -> list:
    jobs = []
    jobs.extend(linkedin.scrape(name, zipcode))
    jobs.extend(glassdoor.scrape(name, zipcode))
    return jobs

def prune_jobs(jobs: list) -> list:
    num_jobs = len(jobs)
    print(f'Pruning {str(num_jobs)} Jobs')
    extras.printProgressBar(0, num_jobs)
    current_job = 0

    pruned_jobs = []
    for job in jobs:
        query = {
            "link": job["link"]
        }
        if db.jobs.count_documents(query) == 0:
            pruned_jobs.append(job)
        
        current_job += 1
        extras.printProgressBar(current_job, num_jobs)
    print(f"Prevented {num_jobs - len(pruned_jobs)} Duplicate Jobs By Pruning")
    return pruned_jobs

def prep_jobs(jobs: list) -> list:
    num_jobs = len(jobs)
    print(f'Prepping {str(num_jobs)} Jobs')
    extras.printProgressBar(0, num_jobs)
    current_job = 0

    prepped_jobs = []
    cities = {}
    for job in jobs:
        location = []
        issue = False
        try:
            location = cities[job['city']]
        except:
            try:
                zipcode = search.by_city_and_state(job['city'], job['state'])[0]
                location = [zipcode.lng, zipcode.lat]
                cities[job['city']] = location
            except:
                issue = True
                print("ISSUE WITH JOB")
                pprint(job)
        job['location'] = {
            'type': 'Point',
            'coordinates': location
        }
        if not issue:
            prepped_jobs.append(job)
        current_job += 1
        extras.printProgressBar(current_job, num_jobs)
    return prepped_jobs

def insert_jobs(jobs: list):
    num_jobs = len(jobs)
    print(f'Inserting {str(num_jobs)} Jobs')
    extras.printProgressBar(0, num_jobs)
    current_job = 0
    for job in jobs:
        try:
            db.jobs.insert_one(job)
        except:
            print(f'Error Occurred With Job {current_job + 1}')
        current_job += 1
        extras.printProgressBar(current_job, num_jobs)

def refresh_job_data(num_queries: int = 20):
    queries = list(db.queue.delete_many({}))
    queries.append(list(db.queries.find({}).sort('date', pymongo.ASCENDING).limit(num_queries - queries.count)))

def perform_query(query: dict, skip_insert: bool = False) -> list:
    name = query['name']
    zipcode = query['zipcode']
    jobs = scrape_for_jobs(name, zipcode)
    jobs = prune_jobs(jobs)
    jobs = prep_jobs(jobs)
    if not skip_insert:
        insert_jobs(jobs)
    return jobs

def perform_queries(queries: list, skip_insert: bool = False):
    for query in queries:
        perform_query(query, skip_insert)

perform_query({'name': 'programmer', 'zipcode': '33480'})
