from bs4 import BeautifulSoup
import requests

url = 'https://career.guru99.com/how-to-answer-50-most-common-interview-questions/'
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
print(soup)
content = soup.findAll('div', class_='entry-content single-content')
print(f"Content {content}")

with open('text.html', 'w', encoding='utf-8') as f:
    indicator = [element for element in content.find_all('h3')]
    print(indicator)

    start_index = content.index(indicator[0])

    endIndex = content.index(indicator[-1])


    for element in content[start_index:endIndex]:
        f.write(f"{element.text}<br>")
        f.write('______________________________________________<br>')

