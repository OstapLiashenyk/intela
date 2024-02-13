from bs4 import BeautifulSoup
import requests

url = 'https://www.codinginterview.com/python-interview-questions'
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

h5 = soup.findAll('span', class_='color_15 wixui-rich-text__text')
answer = soup.findAll('p', class_='font_8 wixui-rich-text__text')
testid = soup.findAll('div', attrs={'data-testid': 'richTextElement'})

with open('text.html', 'w', encoding='utf-8') as f:
    f.write('PYTHONPYTHONPYTHONPYTHONPYTHONPYTHONPYTHONPYTHONPYTHONPYTHONPYTHONPYTHONPYTHONPYTHONPYTHONPYTHONPYTHONPYTHONPYTHONPYTHON')


    begin = [element for element in testid if element.text.startswith("1.")]
    end = [element for element in testid if element.text.startswith("Start Studying for Your Python Interview Today")]

    start_index = testid.index(begin[0])

    endIndex = testid.index(end[-1])


    for element in testid[start_index:endIndex]:
        f.write(f"{element.text}<br>")
        f.write('______________________________________________<br>')

