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

session = requests.Session()
#draft_database.create_tables([TestsS])

def get_Links(place):
        links = place.find_all('a')  # Find all <a> tags
        urls = [link.get('href') for link in links if link.get('href')]
        return urls
def get_jobSpider():
    url = 'https://www.indiabix.com/'
    headers = {'User-Agent': UserAgent}  # Corrected header name

    try:
        response = requests.get(url, headers=headers,verify=False)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        #Programming
        row = soup.findAll('div', class_="col-12 col-xxl-4 col-xl-4 col-lg-4 col-md-6 col-sm-6 mt-20")[-6]
        programming = row.find('ul')
        languages = get_Links(programming)

        #Get languages
        for language_url in languages:
            try:
                resp = requests.get(language_url , headers=headers, verify=False)
                sop = BeautifulSoup(resp.text, "html.parser")

                wrapper = sop.find('div', class_ = "topics-wrapper")
                div = wrapper.find('ul', class_ = "need-ul-filter")
                topics = get_Links(div)

                #Get Topics
                for topic_url in topics:
                    try:
                        print(topic_url)
                        resp = requests.get(topic_url, headers=headers, verify=False)
                        sop = BeautifulSoup(resp.text, "html.parser")
                        exercises = sop.find('div', class_ = "scrolly-250 scrolly-bg1")
                        pages = get_Links(exercises)

                        questions = []

                        pageQuestion = getPageQuestions(topic_url)
                        for question in pageQuestion:
                            questions.append(question)
                            print(question)

                        # for question in questions:
                        #     print(question)

                        for page_url in pages:
                            resp = requests.get(page_url, headers=headers, verify=False)
                            sop = BeautifulSoup(resp.text, "html.parser")

                            pageQuestion = getPageQuestions(page_url)

                            for question in pageQuestion:
                                questions.append(question)
                                print(question)
                    except Exception as err:
                        print(f'UMPALUMPA Error fetching or parsing page at {page_url}: {err}')
                print("________________________________________________________________")


            except Exception as err:
                print(f'UMPALUMPA Error fetching or parsing topic at {topic_url}: {err}')


    except requests.HTTPError as http_err:
        print(f'UMPALUMPA HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'UMPALUMPA Other error occurred: {err}')
#Here to code
print('I Do start')
get_jobSpider()