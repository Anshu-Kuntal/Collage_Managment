# student_management.py
import sqlite3
from database import connect_db
from utils import input_int

def add_student():
    conn = connect_db()
    cursor = conn.cursor()
    name = input("Name: ")
    roll_no = input("Roll No: ")
    cursor.execute("SELECT id, course_name FROM courses ORDER BY course_name ASC")
    courses = cursor.fetchall()
    if not courses: print("❌ Add courses first."); conn.close(); return
    print("\nCourses:")
    for cid, cname in courses: print(f"{cid}: {cname}")
    course_id = input_int("Course ID: ")
    year_or_sem = input("Year/Semester: ")
    total_fees = input_int("Total Fees: ")
    fees_paid = input_int("Fees Paid: ")
    try:
        cursor.execute("""
            INSERT INTO students (name, roll_no, course_id, year_or_sem, total_fees, fees_paid)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, roll_no, course_id, year_or_sem, total_fees, fees_paid))
        conn.commit()
        print("✅ Student added.")
    except sqlite3.IntegrityError as e: print("❌", e)
    conn.close()

def view_students():
    conn = connect_db()
    cursor = conn.cursor()
    course_filter = input("Course ID (or Enter all): ").strip()
    year_filter = input("Year/Sem (or Enter all): ").strip()
    query = """SELECT students.id, students.name, students.roll_no, courses.course_name,
               students.year_or_sem, students.total_fees, students.fees_paid
               FROM students LEFT JOIN courses ON students.course_id=courses.id"""
    params = []
    if course_filter and year_filter: query += " WHERE course_id=? AND year_or_sem=?"; params=[course_filter, year_filter]
    elif course_filter: query += " WHERE course_id=?"; params=[course_filter]
    elif year_filter: query += " WHERE year_or_sem=?"; params=[year_filter]
    cursor.execute(query, tuple(params))
    students = cursor.fetchall()
    if students:
        print("+----+----------------+-----------+----------------+--------------+------------+------------+")
        print("| ID | Name           | Roll No   | Course         | Year/Sem     | Total Fees | Fees Paid  |")
        print("+----+----------------+-----------+----------------+--------------+------------+------------+")
        for s in students: print(f"| {s[0]:<2} | {s[1]:<14} | {s[2]:<9} | {s[3]:<14} | {s[4]:<12} | {s[5]:<10} | {s[6]:<10} |")
        print("+----+----------------+-----------+----------------+--------------+------------+------------+")
    else: print("📂 No records.")
    conn.close()

def update_student():
    conn = connect_db(); cursor = conn.cursor(); roll_no = input("Roll No to update: ")
    cursor.execute("SELECT * FROM students WHERE roll_no=?", (roll_no,))
    student = cursor.fetchone()
    if not student: print("❌ Not found."); conn.close(); return
    name = input(f"Name ({student[1]}): ") or student[1]
    year_or_sem = input(f"Year/Sem ({student[4]}): ") or student[4]
    total_fees = input(f"Total Fees ({student[5]}): ") or student[5]
    fees_paid = input(f"Fees Paid ({student[6]}): ") or student[6]
    cursor.execute("""
        UPDATE students SET name=?, year_or_sem=?, total_fees=?, fees_paid=? WHERE roll_no=?
    """, (name, year_or_sem, total_fees, fees_paid, roll_no))
    conn.commit(); print("✅ Updated."); conn.close()

def delete_student():
    conn = connect_db(); cursor = conn.cursor(); roll_no = input("Roll No to delete: ")
    cursor.execute("DELETE FROM students WHERE roll_no=?", (roll_no,))
    conn.commit()
    print("✅ Deleted." if cursor.rowcount else "❌ Not found.")
    conn.close()

def student_menu():
    while True:
        print("\n🎓 Student Menu:")
        print("1. Add Student\n2. View Students\n3. Update\n4. Delete\n5. Go Back")
        choice = input("Choice (1-5): ").strip()
        if choice=="1": add_student()
        elif choice=="2": view_students()
        elif choice=="3": update_student()
        elif choice=="4": delete_student()
        elif choice=="5": break
        else: print("❌ Invalid.")
