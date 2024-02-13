from bs4 import BeautifulSoup
import requests



url = 'https://hackr.io/blog/programming-interview-questions'
page = requests.get(url)

if page.status_code == 200:

    soup = BeautifulSoup(page.text, 'html.parser')
    h4_tags = soup.findAll('h4')
    ##start = soup.find('h4').index(h4_tags[0])
    #end = soup.find('h4').index(h4_tags[46])
    #print(start)
    #print(end)
    #######result = soup[soup.find[h4_tags[0]]:]]

    with open('index.html', 'w', encoding='utf-8') as f:

        # After 45 is code questions
        for element in h4_tags:
            f.write(f"{element}<br>")
            f.write('______________________________________________<br>')

else:
    with open(f'index.html.html', 'w', encoding='utf-8') as f:

        f.write('Can not get the page')