import sqlite3


BALANCE = 1000


def initiate_db():
    connection = sqlite3.connect('TG_database.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY NOT NULL UNIQUE, 
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL);
        ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY NOT NULL UNIQUE, 
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL);
            ''')
    products_count = cursor.execute("SELECT COUNT(*) FROM Products").fetchone()[0]

    if products_count == 0:
        for i in range(1, 5):
            cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                           (f'Таблетки №{i}', f'Добавят вам калорий: {i * 150}', f'{i * 100}'))
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('TG_database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    all_p = cursor.fetchall()
    connection.commit()
    connection.close()
    return all_p


def add_user(username, email, age):
    connection = sqlite3.connect('TG_database.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (username, email, age, BALANCE))
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect('TG_database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    result = cursor.fetchone()
    connection.close()
    if result is None:
        return False
    return True


initiate_db()
