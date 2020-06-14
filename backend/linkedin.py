import datetime
import json
import urllib.request
from pprint import pprint

from bs4 import BeautifulSoup


# takes 3 arguments: keywords (search term), zip code as location, and number of pages to parse (25 results per page)
# optional LinkedIn jobs API: https://developer.linkedin.com/docs/v1/jobs/job-search-api
def scrape(keywords, zip_code = None, num_pages = 10):
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

        html = urllib.request.urlopen(url).read().decode("utf-8")
        soup = BeautifulSoup(html, features="html.parser")

        card_class = "job-result-card"
        card_prefix = card_class + "__"
        cards = soup.find_all(attrs={"class": card_class})

        jobs_content = [card.contents for card in cards]

        for job_content in jobs_content:
            try:
                if (len(job_content) == 0): continue

                link_tag = job_content[0]
                info_tag = job_content[2]

                dic = {}
                full_link = str(link_tag.get("href"))
                no_tracking_link = full_link.split('?')[0]
                dic["link"] = no_tracking_link

                name_tag, company_tag, metadata_tag = info_tag.contents

                # get unique fields
                # unique_fields = set()
                # for md in metadata_tag.contents:
                #     field = md.get("class")[0][17:]
                #     unique_fields.add(field)

                dic["name"] = name_tag.string
                dic["employer"] = company_tag.string

                locations = metadata_tag.find_all(attrs={"class": card_prefix + "location"})[0].string.split(', ')
                dic["city"] = locations[0]
                dic["state"] = locations[1]

                salary_info = metadata_tag.find_all(attrs={"class": card_prefix + "salary-info"})
                if len(salary_info) == 1:
                    dic["salary"] = salary_info[0].string

                time = metadata_tag.find_all('time')[0]
                #dic["date"] = time.get("datetime")
                #dic["ago"] = time.string

                dic["misc"] = {}
                easy_apply = metadata_tag.find_all(attrs={"class": card_prefix + "easy-apply-label"})
                if len(easy_apply) == 1:
                    dic["misc"]["easy_apply"] = True
                dic['date'] = datetime.datetime.utcnow()

                jobs.append(dic)
            except: 
                print("Error With Job")
                pprint(job_content)
    return jobs

if __name__ == "__main__":
    print(scrape('software', num_pages=1))
