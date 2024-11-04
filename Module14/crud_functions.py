import sqlite3

connection = sqlite3.connect('TG_database.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY NOT NULL UNIQUE, 
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL);
        ''')
    cursor.execute("SELECT COUNT(*) FROM Products")
    count = cursor.fetchone()[0]

    if count == 0:
        for i in range(1, 5):
            cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                           (f'Таблетки №{i}', f'Добавит вам калорий: {i * 150}', f'{i * 100}'))
        connection.commit()


def get_all_products():
    cursor.execute("SELECT * FROM Products")
    all_p = cursor.fetchall()
    connection.close()
    return all_p


initiate_db()


