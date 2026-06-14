import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT,
    quantity INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    class_name TEXT,
    email TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS issued_books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    book_id INTEGER,
    issue_date TEXT,
    due_date TEXT,
    status TEXT DEFAULT 'Issued'
)
''')

conn.commit()
conn.close()

print("Database Created Successfully!")