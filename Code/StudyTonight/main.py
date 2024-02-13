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
subjects = {"java","cpp","c","dbms","computer-networks","operating-system","gate","servlet","engg-maths","android","computer-architecture","data-structures","aptitude","python","big-data","linux"}

subject = 'java'
testNum = '1'

url = f'https://www.studytonight.com/{subject}/tests/{testNum}'
page = requests.get(url)
if page.status_code == 200:
    soup = BeautifulSoup(page.text, 'html.parser')

    questions = soup.findAll('div', class_='quiz_content')
    ans_url = f'https://www.studytonight.com/{subject}/tests/{testNum}_answer.json'
    answers = requests.get(ans_url).json()



    with open(f'{subject}{testNum}.html', 'w', encoding='utf-8') as f:
        jsonCounter = 0


        for element in questions:
            #HTML-----------------------------------------------------------------------------------
            f.write(f"{element}<br>")
            ##Answer type 1:
            f.write(f'{str(answers[jsonCounter])[36]}<br>')
            ## Answer type 2
            f.write(f'{answers[jsonCounter]}<br>')
            f.write('______________________________________________<br>')

            #SQL ------------------------------------------------------------------------------------
            sql = "INSERT INTO question (text,Answer, Correct, Category_idCategory) VALUES (%s, %s,%s,%s)"
            val = (element.text.split('?')[0].strip(), element.text.split('?')[1].strip(), str(answers[jsonCounter])[36], 4)
            mycursor.execute(sql, val)


            jsonCounter+=1
else:
    with open(f'{subject}.html', 'w', encoding='utf-8') as f:

        f.write(f'{subject} , {testNum}, Can not get the page')


mycursor.execute("SELECT * FROM question")
for x in mycursor:
  print(x)

#conn.commit()




