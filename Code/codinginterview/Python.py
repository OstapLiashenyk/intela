from bs4 import BeautifulSoup
import requests
import mysql.connector


conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='1111',
    database='mydb'
)
print(conn)

mycursor = conn.cursor()
print(mycursor)


url = 'https://www.codinginterview.com/python-interview-questions'
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

h5 = soup.findAll('span', class_='color_15 wixui-rich-text__text')
answer = soup.findAll('p', class_='font_8 wixui-rich-text__text')
testid = soup.findAll('div', attrs={'data-testid': 'richTextElement'})

with open('Python.html', 'w', encoding='utf-8') as f:

    begin = [element for element in testid if element.text.startswith("1.")]
    end = [element for element in testid if element.text.startswith("Start Studying for Your Python Interview Today")]

    start_index = testid.index(begin[0])

    endIndex = testid.index(end[-1])

    questionDB = ""
    answerDB = ""
    for element in testid[start_index:endIndex]:
        if element.text[1] == "." or element.text[2] == ".":
            questionDB = element.text[2:]

            if answerDB != "":
                # SQL ------------------------------------------------------------------------------------
                sql = "INSERT INTO question (text,Answer, Correct, Category_idCategory) VALUES (%s, %s,%s,%s)"
                val = (questionDB, answerDB, answerDB, 3)
                mycursor.execute(sql, val)
            answerDB = ""
        else:
            answerDB += element.text
        f.write(f"{element.text}<br>")
        f.write('______________________________________________<br>')

mycursor.execute("SELECT * FROM question")
for x in mycursor:
  print(x)