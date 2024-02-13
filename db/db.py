import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='1111',
    database='mydb'
)

print(conn)

mycursor = conn.cursor()




mycursor.execute("SELECT * FROM category")


for x in mycursor:
  print(x)






