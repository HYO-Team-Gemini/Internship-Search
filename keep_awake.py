from urllib import request

print('Keeping Server Awake')
request.urlopen('https://gemini-jobs.herokuapp.com/jobs')
