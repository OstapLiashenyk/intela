import sys
import inspect
import requests
from datetime import datetime
import re
import urllib.parse
from connections import draft_database
from bs4 import BeautifulSoup
from markdownify import markdownify, UNDERSCORE


def getQuestions(url):
    # Використовуємо бібліотеку requests для отримання вмісту веб-сторінки
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    # print(response.status_code)
    html_content = response.content

    # Створюємо об'єкт BeautifulSoup для парсингу HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Знаходимо всі елементи з класом 'wp-block-heading'
    headings = soup.find_all(class_='wp-block-heading')

    # Ініціалізуємо порожній масив для збереження питань і відповідей
    questions_and_answers = []

    # Проходимо по знайденим елементам і зберігаємо дані в масив
    for i, heading in enumerate(headings):
        question = heading.text.strip()

        # Знаходимо наступний елемент після питання (всі елементи до наступного питання)
        answer_elements = []
        next_element = heading.find_next_sibling()
        while next_element and next_element.name != 'div' and 'wp-block-heading' not in next_element.get('class', []):
            answer_elements.append(next_element)
            next_element = next_element.find_next_sibling()

        # Об'єднуємо всі елементи в один рядок (відповідь)
        answer = ' '.join(element.text.strip() for element in answer_elements)

        # Додаємо питання і відповідь в масив
        questions_and_answers.append(question)
        questions_and_answers.append(answer)

    return questions_and_answers

result = getQuestions('https://www.mygreatlearning.com/blog/python-interview-questions/')
print(result)


