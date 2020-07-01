import json
from pprint import pprint

import pymongo
from uszipcode import SearchEngine, Zipcode
from flask_restful import HTTPException

if __name__ == "__main__":
    import extras, glassdoor, linkedin
else:
    from backend import extras, glassdoor, linkedin

credentials = json.load(open('backend/credentials.json'))
username = credentials['MongoDB']['Username']
password = credentials['MongoDB']['Password']

def get_mongo_client():
    client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@ekko-test-qbczn.mongodb.net/jobs?retryWrites=true&w=majority")
    return client

search = SearchEngine(db_file_dir="backend/tmp")

def scrape_for_jobs(name: str, coordinates: list) -> list:
    lon = coordinates[0]
    lat = coordinates[1]
    zipcode = search.by_coordinates(lat, lon)[0].zipcode
    return scrape_for_jobs(name, zipcode)

def scrape_for_jobs(name: str, zipcode: str) -> list:
    print(f'Starting Scrape For: {name} in {zipcode}')
    jobs = []
    linkedin_failed = False
    try:
        jobs.extend(linkedin.scrape(name, zipcode))
    except:
        linkedin_failed = True
    try:
        jobs.extend(glassdoor.scrape(name, zipcode))
    except:
        if linkedin_failed:
            raise HTTPException(description="Scraping for new data failed", response=500)
    return jobs

def prune_jobs(jobs: list) -> list:
    client = get_mongo_client()
    db = client.jobs

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
    client.close()
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
                print(f"{job['city']}, {job['state']} was not found as a valid city/state pair")
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
    client = get_mongo_client()
    db = client.jobs
    num_jobs = len(jobs)
    print(f'Inserting {str(num_jobs)} Jobs')
    extras.printProgressBar(0, num_jobs)
    current_job = 0
    for job in jobs:
        try:
            db.jobs.insert_one(job)
        except Exception as e:
            print(f'Error Inserting Job {current_job + 1} Into Collection')
            print(str(e))
        current_job += 1
        extras.printProgressBar(current_job, num_jobs)
    num_total = db.jobs.count({})
    print(f'Database Now Has {num_total} Jobs')
    client.close()

def perform_query(query: dict, skip_insert: bool = False) -> list:
    search_engine = SearchEngine(db_file_dir="backend/tmp")

    name = query['name']
    zipcode = query['zipcode']
    jobs = scrape_for_jobs(name, zipcode)
    if len(jobs) > 0:
        jobs = prune_jobs(jobs)
    if len(jobs) > 0:
        jobs = prep_jobs(jobs)
    if not skip_insert and len(jobs) > 0:
        insert_jobs(jobs)
    return jobs

def perform_queries(queries: list, skip_insert: bool = False):
    for query in queries:
        perform_query(query, skip_insert)

if __name__ == "__main__":
    perform_query({'name': 'programmer', 'zipcode': '33480'})

