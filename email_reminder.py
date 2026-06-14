import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ==========================
# EMAIL CONFIGURATION
# ==========================

EMAIL_ADDRESS = "yourgmail@gmail.com"
APP_PASSWORD = "your_app_password"

# ==========================
# DATABASE CONNECTION
# ==========================

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
SELECT
    students.name,
    students.email,
    books.title,
    issued_books.due_date

FROM issued_books

INNER JOIN students
ON students.id = issued_books.student_id

INNER JOIN books
ON books.id = issued_books.book_id

WHERE issued_books.status='Issued'
""")

records = cursor.fetchall()

today = datetime.today().date()


for record in records:

    student_name = record[0]
    student_email = record[1]
    book_title = record[2]
    due_date = record[3]

    due_date_obj = datetime.strptime(
        due_date,
        "%Y-%m-%d"
    ).date()

    days_left = (due_date_obj - today).days

    # Send reminder only if due in next 3     if days_left <= 3:

        subject = "Library Book Return Reminder"

        if days_left >= 0:
            status_message = (
                f"Your book is due in {days_left} day(s)."
            )
        else:
            status_message = (
                f"Your book is overdue by {abs(days_left)} day(s)."
            )

        body = f"""
Hello {student_name},

This is a reminder from the Library Management System.

Book Title:
{book_title}

Due Date:
{due_date}

{status_message}

Please return the book as soon as possible.

Thank You,
Library Administration
"""

        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = student_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        try:

            server = smtplib.SMTP(
                "smtp.gmail.com",
                587
            )

            server.starttls()

            server.login(
                EMAIL_ADDRESS,
                APP_PASSWORD
            )

            server.send_message(msg)

            server.quit()

            print(
                f"Reminder sent to {student_email}"
            )

        except Exception as e:

            print(
                f"Failed to send email to "
                f"{student_email}"
            )

            print(e)

conn.close()

print("Reminder process completed.")