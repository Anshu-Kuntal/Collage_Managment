from database import connect_db
from tabulate import tabulate


# ------------------- STUDENT LOGIN -------------------

def student_login():
    conn = connect_db()
    cursor = conn.cursor()

    roll_no = input("🎓 Enter Roll No: ").strip()
    mobile = input("📱 Enter Mobile No: ").strip()

    cursor.execute("""
        SELECT * FROM students
        WHERE roll_no=? AND mobile=?
    """, (roll_no, mobile))

    student = cursor.fetchone()
    conn.close()

    if student:
        print("✅ Login successful!")
        return student   # return full student data

    print("❌ Invalid credentials")
    return None


# ------------------- VIEW PROFILE -------------------

def view_profile(student):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT students.name,
               students.roll_no,
               students.father_name,
               students.mobile,
               courses.course_name,
               students.year_or_sem,
               students.total_fees,
               students.fees_paid
        FROM students
        LEFT JOIN courses ON students.course_id = courses.id
        WHERE students.id=?
    """, (student[0],))

    data = cursor.fetchone()

    if data:
        due = data[6] - data[7]
        status = "Paid" if due == 0 else "Due"

        print(tabulate(
            [(*data, status)],
            headers=["Name","Roll No","Father","Mobile","Course","Sem","Total","Paid","Status"],
            tablefmt="grid"
        ))

    conn.close()


# ------------------- VIEW ATTENDANCE -------------------

def view_attendance(student):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, subject, status
        FROM attendance
        WHERE student_id=?
        ORDER BY date DESC
    """, (student[0],))

    rows = cursor.fetchall()

    if rows:
        print(tabulate(
            rows,
            headers=["Date","Subject","Status"],
            tablefmt="grid"
        ))
    else:
        print("📂 No attendance records.")

    conn.close()


# ------------------- VIEW RESULT -------------------

def view_result(student):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subject, marks, max_marks
        FROM results
        WHERE student_id=?
    """, (student[0],))

    rows = cursor.fetchall()

    if rows:
        print(tabulate(
            rows,
            headers=["Subject","Marks","Max Marks"],
            tablefmt="grid"
        ))
    else:
        print("📂 No results found.")

    conn.close()