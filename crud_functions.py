import sqlite3


def initiate_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL 
    )
    ''')

    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.close()
    return products


def database_add():
    for i in range(1, 5):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Products (title, description, price) VALUES(?, ?, ?)",
                       (f'User{i}', f'example{i}@gmail.com', f'{i * 10}'))
        connection.commit()
        connection.close()
