import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY NOT NULL UNIQUE, 
username TEXT NOT NULL,
email TEXT NOT NULL,
age	INTEGER,
balance INTEGER NOT NULL
)
''')

for i in range(1, 11):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (f'User{i}', f'example{i}@gmail.com', i * 10, 1000))

cursor.execute("UPDATE Users SET balance = 500 WHERE id % 2 != 0")

cursor.execute("SELECT COUNT(*) FROM Users")
row_num = cursor.fetchone()[0]

for i in range(1, row_num + 1, 3):
    cursor.execute(f"DELETE FROM Users WHERE id = {i}")

cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != 60")
users = cursor.fetchall()
for user in users:
    username, email, age, balance = user
    print(f"Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}")

connection.commit()
connection.close()