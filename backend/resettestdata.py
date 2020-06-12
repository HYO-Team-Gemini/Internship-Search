import json
import pymongo
import random
from datetime import datetime, timedelta

credentials = json.load(open('backend/credentials.json'))
username = credentials['MongoDB']['Username']
password = credentials['MongoDB']['Password']
client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@ekko-test-qbczn.mongodb.net/jobs?retryWrites=true&w=majority")
db = client.test

companies = ['Google', 'Facebook', 'Amazon', 'Apple', 'Reddit', 'Discord', 'LinkedIn', 'Alibaba', 'Activision', 'Blizzard Entertainment']
job_titles = ['Software Engineer', 'DevOps', 'HR Representative', 'Project Lead', 'Systems Architect', 'UI/UX Designer', 'Senior Developer', 'Graphics Team Lead']
websites = ['linkedin.com', 'glassdoor.com']
base_location = credentials["Personal"]["Coordinates"]

 ##db.jobs.delete_many({})

def create_job(title: str, company: str, location: list, website: str, date: datetime) -> dict:
    job = {
        'name': title,
        'employer': company,
        'link': website,
        'location': {
            'type': 'Point',
            'coordinates': location
        },
        'date': date
    }
    return job

for company in companies:
    for job_title in job_titles:
        for website in websites:
            date = datetime.utcnow() - timedelta(days=random.randint(0, 70))
            location = [base_location[0] + (random.random() - 0.5) * 8, base_location[1] + (random.random() - 0.5) * 8]
            job = create_job(job_title, company, location, website, date)
            db.jobs.insert_one(job)

        
