from bs4 import BeautifulSoup
import requests

url = 'https://www.codinginterview.com/algorithms'
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')


testid = soup.findAll('div', attrs={'data-testid': 'richTextElement'})

with open('Algorithms.html', 'w', encoding='utf-8') as f:
    f.write('AlgorithmsAlgorithmsAlgorithmsAlgorithmsAlgorithms<br>')

    begin = [element for element in testid if element.text.startswith("1.")]
    end = [element for element in testid if element.text.startswith("conclusion")]

    start_index = testid.index(begin[0])

    endIndex = testid.index(end[-1])


    for element in testid[start_index:endIndex]:
        f.write(f"{element.text}<br>")
        f.write('______________________________________________<br>')

