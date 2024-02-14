import sys
import inspect
import requests
from datetime import datetime
import re
import urllib.parse
from connections import draft_database
from bs4 import BeautifulSoup
from models.tests import TestsS
from getPage.test import getPageQuestions


UserAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

now = datetime.now().replace(second=0, microsecond=0)
print(now)

draft_database.create_tables([TestsS])
print(123)
def get_Links(place):
        links = place.find_all('a')  # Find all <a> tags
        urls = [ f"https://www.jobspider.com/{link.get('href')}" for link in links if link.get('href') and link.get('href') != "#"]
        return urls
def get_jobSpider(url):
    headers = {'User-Agent': UserAgent}  # Corrected header name
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        main_block = soup.find_all('font', face = 'arial', size ='2')[1]
        links = get_Links(main_block)
        pages_links = []
        for link in links:
            if link in pages_links:
                continue
            if "page" in link:
                pages_links.append(link)
                print(f' page = {link}')

        page_number = 1
        while True:
            resums_tbale = main_block.find('table', border="1", cellpadding="2", cellspacing="0", bordercolor="#336699", width="100%")
            resums = resums_tbale.find('tr').find_next_siblings()
            for resum in resums:
                columns = resum.find_all('td')
                id = columns[0]
                posted = columns[1]
                jobFunctionSought = columns[2]
                desiredIndustry = columns[3]
                location = columns[4]
                resume_link = get_Links(columns[5])

                print(id, posted, jobFunctionSought ,desiredIndustry, location, resume_link)
                resume = getPageQuestions(resume_link[0])
                resume.id = id
                resume.posted = posted
                resume.jobFunctionSought = jobFunctionSought
                resume.desiredIndustry = desiredIndustry
                resume.location = location
                print(resume)

                rc1 = TestsS.insert({
                    #'id' : resume.id.text,
                    'posted' : resume.posted,
                    'jobFunctionSough' : resume.jobFunctionSought,
                    'desiredIndustry' : resume.desiredIndustry,
                    'location' : resume.location,
                    'objective' : resume.objective,
                    'experience' : resume.experience,
                    'education' : resume.education,
                    'affiliations' : resume.affiliations,
                    'skills' : resume.skills,
                    'additionalInformation' : resume.additionalInformation,
                    'reference' : resume.reference
                }).on_conflict_ignore().as_rowcount().execute()
                print(resume.id.text , ' ',resume.objective ,' ', rc1)
                print(123)
            if page_number > 0:
                break

    except Exception as err:
        print(f'UMPALUMPA Other error occurred: {err}')

#Here to code
print('I Do start')
get_jobSpider('https://www.jobspider.com/job/resume-search-results.asp/category_121')