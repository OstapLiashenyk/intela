import sys
import inspect
import requests
from datetime import datetime
import re
import urllib.parse
import time
from connections import draft_database
from bs4 import BeautifulSoup
from markdownify import markdownify, UNDERSCORE

from models.tests import TestsS
from models.tests import QnrSingleSelectItem, QnrSingleAnswerOption
from mgltest.test import getQuestions



UserAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

now = datetime.now().replace(second=0, microsecond=0)
print(now)

session = requests.Session()

draft_database.create_tables([TestsS])
#draft_database.create_tables([QnrSingleSelectItem, QnrSingleAnswerOption])



def get_studytonight_by_page():
    url = 'https://www.mygreatlearning.com/blog/python-interview-questions/'
    headers = {'UserAgent': UserAgent}
    while True:
        with session.get(f"{url}",
                         headers=headers) as response:
            if response.status_code == 200:
                try:
                    soup = BeautifulSoup(response.text, "html.parser")

                    quick_links_div = soup.find('div', class_='quick-links')
                    if quick_links_div:
                        links = quick_links_div.find_all('a')
                        for link in links:
                            href = link.get('href')
                            with session.get(f"{href}", headers=headers) as response:
                                if response.status_code == 200:
                                    try:
                                        # Повертаэ масив, де 0 елемент це питання, 1 це выдповідь ітд.
                                        ans = getQuestions(href)
                                        # Записуємо відповіді до БД
                                        tittle = href.split('/')[-2].replace("-interview-questions", "")
                                        for index, element in enumerate(ans):
                                            if index % 2 == 0:
                                                id = f"{tittle}_{str(index // 2 + 1).zfill(3)}"
                                                question = element
                                            else:
                                                answer = element
                                                rc = TestsS.insert({
                                                    'id': id,
                                                    'text': question,
                                                    'answer': answer,
                                                    'topic': tittle}).on_conflict_ignore().as_rowcount().execute()
                                                if rc == 1:
                                                    print(id, ' ', rc)


                                    except Exception as e:
                                        print(e)
                                # else:
                                #     print(href)
                    else:
                        print("Quick-links div not found.")
                except Exception as e:
                    print(e)
                #time.sleep(6)# Виключаємо перенавантаження на сервер
            else:
                print(response.status_code)

        break
while True:
    get_studytonight_by_page()
    print(f'i go to sleep')
    for i in range(3):
        time.sleep(300)
    print('here am i')
# def get_studytonight_by_page():
#
#     url = 'https://www.mygreatlearning.com/blog/embedded-c-interview-questions/'
#     headers = {'UserAgent': UserAgent}
#     while True:
#         with session.get(f"{url}",
#                          headers=headers) as response:
#             if response.status_code == 200:
#                 try:
#                     soup = BeautifulSoup(response.text, "html.parser")
#                     hrefs = soup.find(id='test-list').find_all(href=True, class_=lambda x: x != 'page-link')


#                     for i, href in enumerate(hrefs):
#                         with session.get(f"{url}{href.get('href')}", headers=headers) as response:
#                             if response.status_code == 200:
#                                 soup2 = BeautifulSoup(response.text, "html.parser")
#                                 id = f"{topic}_{str(page).zfill(2)}_{str(i + 1).zfill(2)}"
#                                 level = href.find('span', title='Difficulty Level').get_text().strip(),
#                                 rc = TestsS.insert({
#                                     'id': id,
#                                     'title': (title := href.find('h2').get_text().strip()),
#                                     'level': level,
#                                     'avg_score': re.sub(r'[^\d]*', '', href.find('span', string=re.compile('Score',
#                                                                                                            re.IGNORECASE)).get_text()),
#                                     'attempts': href.find('span', title='Number of times attempted').get_text().strip(),
#                                     'topic': topic}).on_conflict_ignore().as_rowcount().execute()
#                                 with session.get(f"{url}{href.get('href')}_answer.json", headers=headers) as response2:
#                                     if response2.status_code == 200:
#                                         answers = response2.json()  # json.loads(re.sub(r'([=a-z])"(?!\n)([\sa-z])', r'\1\"\2', re.sub(r'\\', r'\\\\', response2.text)))
#                                         for j, container in enumerate(soup2.find_all(class_='quiz_content')):
#                                             q_id = f"{id}_q{j + 1}"
#                                             print(q_id)
#                                             try:
#                                                 # question = container.find(class_='quiz_question')
#                                                 question = container.select(
#                                                     '.quiz_content > :not(.quiz_options):not(.quiz_answer_holder)') or ''
#                                                 options = container.find(class_='quiz_options')
#                                                 # options = container.find_all(class_=lambda x: x in ('quiz_options', 'code-toolbar'), recursive=False)
#                                                 rc2 = TestQuestionsS.insert({
#                                                     'id': q_id,
#                                                     'question_html': question,
#                                                     'question': '\n'.join([elm.get_text().strip() for elm in question]),
#                                                     'options_html': options,
#                                                     'options': '\n'.join(
#                                                         [option.get_text().strip() for option in options]),
#                                                     'answer': answers[j],
#                                                     'test_id': id
#                                                 }).on_conflict_ignore().as_rowcount().execute()
#                                                 print(q_id, ' ', rc, ' ', rc2)
#
#
#                                             except Exception as e:
#                                                 print(e)
#                 except Exception as e:
#                     print(e)
#                 if len(pages := soup.find(id='Q-list').find_all(href=True, class_='page-link',
#                                                                    string=lambda x: x != 'Next')) > 0 and page < int(
#                         pages[-1].get_text()):
#                     page += 1
#                 else:
#                     break
#
#
#
#
