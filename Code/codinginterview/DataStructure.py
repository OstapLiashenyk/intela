from bs4 import BeautifulSoup
import requests

url = 'https://www.codinginterview.com/data-structures'
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

h5 = soup.findAll('span', class_='color_15 wixui-rich-text__text')
answer = soup.findAll('p', class_='font_8 wixui-rich-text__text')
testid = soup.findAll('div', attrs={'data-testid': 'richTextElement'})

with open('DataStructure.html', 'w', encoding='utf-8') as f:

    begin = [element for element in testid if element.text.startswith("1.")]
    end = [element for element in testid if element.text.startswith("Learn more to ace your interview!")]

    start_index = testid.index(begin[0])
    print(start_index)
    endIndex = testid.index(end[-1])
    print(endIndex)

    for element in testid[start_index:endIndex]:
        f.write(f"{element.text}<br>")
        f.write('______________________________________________<br>')
