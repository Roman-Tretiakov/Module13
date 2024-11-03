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

cursor.execute("DELETE FROM Users WHERE id = 6")

cursor.execute("SELECT COUNT(*) FROM Users")
total_users = cursor.fetchone()[0]

cursor.execute("SELECT SUM(balance) FROM Users")
all_balances = cursor.fetchone()[0]

print(all_balances / total_users)

connection.commit()
connection.close()