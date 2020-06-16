import argparse
import datetime
import json
import os
import random
import re
import sys
import urllib.request
from pprint import pprint

import requests
import unicodecsv as csv
from bs4 import BeautifulSoup
from flask_restful import HTTPException
from lxml import etree, html

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

def get_place_id(place: str) -> str:
	location_headers = {
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.01',
		'accept-encoding': 'gzip, deflate, sdch, br',
		'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
		'referer': 'https://www.glassdoor.com/',
		'upgrade-insecure-requests': '1',
		'user-agent': random.choice(user_agent_list),
		'Cache-Control': 'no-cache',
		'Connection': 'keep-alive'
	}

	data = {
		"term": place,
		"maxLocationsToReturn": 10
	}

	location_url = "https://www.glassdoor.co.in/findPopularLocationAjax.htm?"

	try:
		location_response = requests.post(location_url, headers=location_headers, data=data).json()
		place_id = location_response[0]['locationId']
	except:
		raise HTTPException(description=f'Error Loading Glassdoor Location Data For: {place}', response=500)

	return place_id

def scrape(keyword: str = 'job', place: str = 'us') -> list:

	place_id = get_place_id(place)

	job_litsting_url = 'https://www.glassdoor.com/Job/jobs.htm'
	# Form data to get job results
	data = {
		'clickSource': 'searchBtn',
		'sc.keyword': keyword,
		'locT': 'C',
		'locId': place_id,
		'jobType': ''
	}

	headers = {	
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'accept-encoding': 'gzip, deflate, sdch, br',
		'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
		'referer': 'https://www.glassdoor.com/',
		'upgrade-insecure-requests': '1',
		'user-agent': random.choice(user_agent_list),
		'Cache-Control': 'no-cache',
		'Connection': 'keep-alive'
	}
	response = requests.post(job_litsting_url, headers=headers, data=data)
	# extracting data from
	# https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=true&clickSource=searchBtn&typedKeyword=andr&sc.keyword=android+developer&locT=C&locId=1146821&jobType=
	parser = html.fromstring(response.text)
	# Making absolute url
	base_url = "https://www.glassdoor.com"
	parser.make_links_absolute(base_url)

	XPATH_ALL_JOB = '//li[@class="jl"]'
	XPATH_NAME = './/a/text()'
	XPATH_JOB_URL = './/a/@href'
	XPATH_LOC = './/span[@class="subtle loc"]/text()'
	XPATH_COMPANY = './/div[@class="flexbox empLoc"]/div/text()'
	XPATH_SALARY = './/span[@class="green small"]/text()'

	listings = parser.xpath(XPATH_ALL_JOB)

	job_listings = []
	
	for job in listings:
		raw_job_name = job.xpath(XPATH_NAME)
		raw_job_url = job.xpath(XPATH_JOB_URL)
		raw_lob_loc = job.xpath(XPATH_LOC)
		raw_company = job.xpath(XPATH_COMPANY)
		raw_salary = job.xpath(XPATH_SALARY)

		# Cleaning data
		#getting rid of chars like -
		job_name = ''.join(raw_job_name).strip('–') if raw_job_name else None
		job_location = ''.join(raw_lob_loc) if raw_lob_loc else None
		raw_state = re.findall(",\s?(.*)\s?", job_location)
		state = ''.join(raw_state).strip()
		raw_city = job_location.replace(state, '')
		city = raw_city.replace(',', '').strip()
		company = ''.join(raw_company).replace('–','')
		salary = ''.join(raw_salary).strip()
		job_url = raw_job_url[0] if raw_job_url else None

		job_url = requests.get(job_url, headers= headers, allow_redirects=True).url
		job_url = job_url.split('&ctt=')[0]

		job_cleaned = {
			"name": job_name,
			"employer": company,
			"state": state,
			"city": city,
			"salary": salary,
			"link": job_url,
			"date": datetime.datetime.utcnow()
		}
		
		job_listings.append(job_cleaned)

	return job_listings

if __name__ == "__main__":
	pprint(scrape('software', '33480'))
