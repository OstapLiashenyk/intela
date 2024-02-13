import sys
import inspect
import requests
from datetime import datetime
import re
import urllib.parse
from connections import draft_database
from bs4 import BeautifulSoup
from markdownify import markdownify, UNDERSCORE

from models.tests import TestsS, TestQuestionsS
from models.tests import QnrSingleSelectItem, QnrSingleAnswerOption

UserAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

now = datetime.now().replace(second=0, microsecond=0)
print(now)

session = requests.Session()

draft_database.create_tables([TestsS, TestQuestionsS])
draft_database.create_tables([QnrSingleSelectItem, QnrSingleAnswerOption])

url = 'https://www.indeed.com/hire/interview-questions'
headers = {'UserAgent': UserAgent}

with session.get(f"{url}" ,headers=headers) as response:
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup)