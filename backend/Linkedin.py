from bs4 import BeautifulSoup
<<<<<<< HEAD
import urllib.request
=======
import urllib3
>>>>>>> abaf703ce858c169c68cbf487d387acdf60e3f93
import json

http = urllib3.PoolManager()
# takes 3 arguments: keywords (search term), zip code as location, and number of pages to parse (25 results per page)
# optional LinkedIn jobs API: https://developer.linkedin.com/docs/v1/jobs/job-search-api
def linkedin_scrape(keywords, zip_code = None, num_pages = 10):
    # build query
    query = "keywords=" + "%20".join(str.split(keywords))
    if zip_code:
        query += "&location=" + str(zip_code)

    base_url = ("https://www.linkedin.com/jobs/search?" + query
             + "&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=")

    jobs = []

    # iterate through specified number of pages to get job results
    for page_number in range(0, num_pages):
        url = base_url + str(page_number)

<<<<<<< HEAD
        html = urllib.request.urlopen(url).read().decode("utf-8")
=======
        html = http.urlopen('GET', url).data.decode("utf-8") 
>>>>>>> abaf703ce858c169c68cbf487d387acdf60e3f93
        soup = BeautifulSoup(html, features="html.parser")

        card_class = "job-result-card"
        card_prefix = card_class + "__"
        cards = soup.find_all(attrs={"class": card_class})

        jobs_content = [card.contents for card in cards]

        for job_content in jobs_content:
            if (len(job_content) == 0): continue

            link_tag = job_content[0]
            info_tag = job_content[2]

            dic = {}
            dic["Url"] = link_tag.get("href")

            name_tag, company_tag, metadata_tag = info_tag.contents

            # get unique fields
            # unique_fields = set()
            # for md in metadata_tag.contents:
            #     field = md.get("class")[0][17:]
            #     unique_fields.add(field)

            dic["Name"] = name_tag.string
            dic["Company"] = company_tag.string

            dic["Location"] = metadata_tag.find_all(attrs={"class": card_prefix + "location"})[0].string

            salary_info = metadata_tag.find_all(attrs={"class": card_prefix + "salary-info"})
            if len(salary_info) == 1:
                dic["Salary"] = salary_info[0].string

            time = metadata_tag.find_all('time')[0]
            #dic["date"] = time.get("datetime")
            #dic["ago"] = time.string

            dic["Misc"] = {}
            easy_apply = metadata_tag.find_all(attrs={"class": card_prefix + "easy-apply-label"})
            if len(easy_apply) == 1:
                dic["Misc"]["easy_apply"] = True

            jobs.append(dic)


    obj = { "num_jobs": len(jobs), "jobs": jobs }

    with open('linkedin_data.json', 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)
    #Not using Json in this context to keep it consistent with glassdoor.py
    return jobs;
    #Jobs Fields: Url, Name, Company, Location, Salary, Misc, easy_apply
print(linkedin_scrape('software', 33480, 10))