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

def md(text):
    try:
        return markdownify(text.replace('code>', 'em>'), strong_em_symbol=UNDERSCORE)
    except Exception as e:
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()

def get_studytonight_by_page():
    topics = {'java': 'java',
              'cpp': 'c/c++',
              'c': 'c/c++',
              'dbms': 'dbms',
              'computer-networks':'networking',
              'operating-system':'operating_systems',
              #'gate',
              'servlet': 'j2ee',
              'jsp': 'jsp',
              'engg-maths': 'mathematics',
              'android': 'android',
              'computer-architecture': 'computer_science',
              'data-structures': 'data_structures',
              'aptitude': 'mathematics',
              'python': 'python',
              'big-data': 'big_data',
              'linux': 'linux'}
    #'engg-maths','android','computer-architecture','data-structures','aptitude','python','big-data','linux'
    #topics = {k: v for k, v in topics.items() if k in ['android']}

    url = 'https://www.studytonight.com'
    headers = {'UserAgent': UserAgent}
    for topic, skill in topics.items():
        page = 1
        while True:
            with session.get(f"{url}/tests/?{urllib.parse.urlencode({'subject': topic, 'p': page})}", headers=headers) as response:
                if response.status_code == 200:
                    try:
                        soup = BeautifulSoup(response.text, "html.parser")
                        hrefs = soup.find(id='test-list').find_all(href=True, class_=lambda x: x != 'page-link')
                        for i, href in enumerate(hrefs):
                            with session.get(f"{url}{href.get('href')}", headers=headers) as response:
                                if response.status_code == 200:
                                    soup2 = BeautifulSoup(response.text, "html.parser")
                                    id = f"{topic}_{str(page).zfill(2)}_{str(i + 1).zfill(2)}"
                                    level = href.find('span', title='Difficulty Level').get_text().strip(),
                                    rc = TestsS.insert({
                                        'id': id,
                                        'title': (title := href.find('h2').get_text().strip()),
                                        'level': level,
                                        'avg_score': re.sub(r'[^\d]*', '', href.find('span', string=re.compile('Score', re.IGNORECASE)).get_text()),
                                        'attempts': href.find('span', title='Number of times attempted').get_text().strip(),
                                        'topic': topic}).on_conflict_ignore().as_rowcount().execute()
                                    with session.get(f"{url}{href.get('href')}_answer.json", headers=headers) as response2:
                                        if response2.status_code == 200:
                                            answers = response2.json() #json.loads(re.sub(r'([=a-z])"(?!\n)([\sa-z])', r'\1\"\2', re.sub(r'\\', r'\\\\', response2.text)))
                                            for j, container in enumerate(soup2.find_all(class_='quiz_content')):
                                                q_id = f"{id}_q{j+1}"
                                                print(q_id)
                                                try:
                                                    #question = container.find(class_='quiz_question')
                                                    question = container.select('.quiz_content > :not(.quiz_options):not(.quiz_answer_holder)') or ''
                                                    options = container.find(class_='quiz_options')
                                                    #options = container.find_all(class_=lambda x: x in ('quiz_options', 'code-toolbar'), recursive=False)
                                                    rc2 = TestQuestionsS.insert({
                                                        'id': q_id,
                                                        'question_html': question,
                                                        'question': '\n'.join([elm.get_text().strip() for elm in question]),
                                                        'options_html': options,
                                                        'options': '\n'.join([option.get_text().strip() for option in options]),
                                                        'answer': answers[j],
                                                        'test_id': id
                                                    }).on_conflict_ignore().as_rowcount().execute()
                                                    print(q_id, ' ', rc, ' ', rc2)

                                                    # singleItem = QnrSingleSelectItem.insert({
                                                    #     'id': q_id,
                                                    #     'skill_id': skill,
                                                    #     'score': 3 if level == 'Expert' else 2 if level == 'Intermediate' else 1,
                                                    #     'question': ''.join([md(elm.prettify()) for elm in question]),
                                                    #     'explanation': (res:=re.search(r'OPTION \w,(.*)', answers[j].get('answer'))) and res.group(1),
                                                    #     'source': 'studytonight'}).on_conflict_ignore().execute()
                                                    #     #article = '\n'.join([option.get_text().strip() for option in options]),
                                                    # QnrSingleAnswerOption.insert([{
                                                    #     'qnr_item': singleItem or q_id,
                                                    #     'num': num,
                                                    #     'is_correct': re.search(r'OPTION (\w)', answers[j].get('answer')).group(1) == ((res:=re.search(r'^.*([A-G])(?=\.)', option.get_text().strip())) and res.group(1)),
                                                    #     'text': re.sub(r'\|$','',re.sub(r'^\s*__[A-G]\.__\s*','',md(option.prettify()))).strip()
                                                    #     #re.search(r'^[ABCDEF]\.(.*)', option.get_text().strip()).group(1)
                                                    # }
                                                    #         for num, option in enumerate(options.find_all('td'))]).on_conflict(
                                                    #     conflict_target=[QnrSingleAnswerOption.qnr_item,
                                                    #                      QnrSingleAnswerOption.num],
                                                    #     preserve=['text', 'is_correct']).execute()
                                                except Exception as e:
                                                    print(e)
                    except Exception as e:
                        print(e)
                    if len(pages := soup.find(id='test-list').find_all(href=True, class_='page-link', string=lambda x: x != 'Next')) > 0 and page < int(pages[-1].get_text()):
                        page += 1
                    else:
                        break
                else:
                    break


get_studytonight_by_page()