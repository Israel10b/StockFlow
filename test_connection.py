import mysql.connector
from getpass import getpass

connection = mysql.connector.connect(
    host="localhost",
    user=input("MySQL username: "),
    password=getpass("MySQL password: "),
    database="stockflow_db"
)

print("Successfully connected to StockFlow database!")

cursor = connection.cursor(dictionary=True)

cursor.execute("SELECT id, name, total_quantity FROM equipment ORDER by id")

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()

connection.close()