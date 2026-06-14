from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

DB = "database.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db()

    books = conn.execute(
        "SELECT COUNT(*) FROM books").fetchone()[0]

    students = conn.execute(
        "SELECT COUNT(*) FROM students").fetchone()[0]

    issued = conn.execute(
        "SELECT COUNT(*) FROM issued_books WHERE status='Issued'"
    ).fetchone()[0]

    conn.close()

    return render_template(
        'index.html',
        books=books,
        students=students,
        issued=issued
    )


@app.route('/books')
def books():
    conn = get_db()
    books = conn.execute(
        "SELECT * FROM books").fetchall()
    conn.close()
    return render_template(
        'books.html',
        books=books
    )


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():

    if request.method == 'POST':

        title = request.form['title']
        author = request.form['author']
        category = request.form['category']
        quantity = request.form['quantity']

        conn = get_db()

        conn.execute(
            '''
            INSERT INTO books
            (title,author,category,quantity)
            VALUES(?,?,?,?)
            ''',
            (title, author, category, quantity)
        )

        conn.commit()
        conn.close()

        return redirect('/books')

    return render_template('add_book.html')


@app.route('/students', methods=['GET', 'POST'])
def students():

    conn = get_db()

    if request.method == 'POST':

        name = request.form['name']
        class_name = request.form['class_name']
        email = request.form['email']

        conn.execute(
            '''
            INSERT INTO students
            (name,class_name,email)
            VALUES(?,?,?)
            ''',
            (name, class_name, email)
        )

        conn.commit()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return render_template(
        'students.html',
        students=students
    )


@app.route('/issue_book', methods=['GET', 'POST'])
def issue_book():

    conn = get_db()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    books = conn.execute(
        "SELECT * FROM books"
    ).fetchall()

    if request.method == 'POST':

        student_id = request.form['student_id']
        book_id = request.form['book_id']

        issue_date = datetime.now().strftime("%Y-%m-%d")

        due_date = (
            datetime.now() +
            timedelta(days=14)
        ).strftime("%Y-%m-%d")

        conn.execute(
            '''
            INSERT INTO issued_books
            (student_id,book_id,issue_date,due_date)
            VALUES(?,?,?,?)
            ''',
            (
                student_id,
                book_id,
                issue_date,
                due_date
            )
        )

        conn.commit()

        return redirect('/return_book')

    return render_template(
        'issue_book.html',
        students=students,
        books=books
    )


@app.route('/return_book')
def return_book():

    conn = get_db()

    issued = conn.execute(
        '''
        SELECT issued_books.id,
               students.name,
               books.title,
               issue_date,
               due_date
        FROM issued_books
        JOIN students
        ON students.id = issued_books.student_id
        JOIN books
        ON books.id = issued_books.book_id
        WHERE status='Issued'
        '''
    ).fetchall()

    conn.close()

    return render_template(
        'return_book.html',
        issued=issued
    )


@app.route('/return/<int:id>')
def return_book_action(id):

    conn = get_db()

    conn.execute(
        '''
        UPDATE issued_books
        SET status='Returned'
        WHERE id=?
        ''',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/return_book')


if __name__ == '__main__':
    app.run(debug=True)
