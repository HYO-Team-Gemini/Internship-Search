import marshmallow
import json

##TODO: Read Data From MongoDB
jobs = json.load(open('example-models/jobs.json'))['jobs']

def search(args: dict) -> dict:
    filtered_jobs = {}
    for key in jobs:
        job = jobs[key]
        if args['name'] == '*' or args['name'] in job['name']:
            if args['employer'] == '*' or args['employer'] in job['employer']:
                job_id = len(filtered_jobs.keys()) + 1
                filtered_jobs[str(job_id)] = job
    output = { "num_jobs": len(filtered_jobs.keys()), "jobs": filtered_jobs}
    return output

print(search({'name': '*', 'employer': '*'}))