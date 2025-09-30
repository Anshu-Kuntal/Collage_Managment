# result_management.py
import sqlite3
from database import connect_db
from tabulate import tabulate

def add_result():
    conn = connect_db(); cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM students"); students = cursor.fetchall()
    if not students: print("❌ Add students first."); conn.close(); return
    print("\nStudents:"); 
    for sid, sname in students: print(f"{sid}: {sname}")
    student_id = input("Student ID: ")
    cursor.execute("SELECT course_id, year_or_sem FROM students WHERE id=?", (student_id,))
    info = cursor.fetchone()
    if not info: print("❌ Student not found."); conn.close(); return
    course_id, year_or_sem = info
    cursor.execute("SELECT subject_name FROM subjects WHERE course_id=? AND term_number=?", (course_id, year_or_sem))
    subjects = cursor.fetchall()
    if not subjects: print("❌ No subjects."); conn.close(); return
    academic_year = input("Academic Year: ")
    for sub in subjects:
        marks = int(input(f"{sub[0]} Marks: "))
        max_marks = int(input(f"{sub[0]} Max Marks: "))
        cursor.execute("INSERT INTO results (student_id, term_number, academic_year, subject, marks, max_marks) VALUES (?, ?, ?, ?, ?, ?)",
                       (student_id, year_or_sem, academic_year, sub[0], marks, max_marks))
    conn.commit(); print("✅ Result added."); conn.close()

def view_results():
    conn = connect_db(); cursor = conn.cursor()
    student_id = input("Student ID (or Enter all): ").strip()
    query = """
        SELECT students.name, courses.course_name, students.year_or_sem, results.academic_year, results.subject, results.marks, results.max_marks
        FROM results
        JOIN students ON results.student_id=students.id
        JOIN courses ON students.course_id=courses.id
    """
    params = ()
    if student_id: query += " WHERE students.id=?"; params=(student_id,)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    if rows:
        print(tabulate(rows, headers=["Student","Course","Year/Sem","Acad Year","Subject","Marks","Max Marks"], tablefmt="grid"))
    else: print("📂 No results found.")
    conn.close()

def register_re_exam():
    conn = connect_db(); cursor = conn.cursor()
    student_id = input("Student ID: "); subject=input("Subject: ")
    term_number = input("Term/Year: "); academic_year = input("Academic Year: ")
    cursor.execute("INSERT INTO re_exams (student_id, subject, term_number, academic_year, status) VALUES (?, ?, ?, ?, 'Pending')",
                   (student_id, subject, term_number, academic_year))
    conn.commit(); print("✅ Re-Exam registered."); conn.close()

def view_re_exam_status():
    conn = connect_db(); cursor = conn.cursor()
    cursor.execute("""
        SELECT re_exams.id, students.name, re_exams.subject, re_exams.term_number, re_exams.academic_year, re_exams.status
        FROM re_exams
        JOIN students ON re_exams.student_id=students.id
    """)
    rows = cursor.fetchall()
    if rows:
        print(tabulate(rows, headers=["ID","Student","Subject","Term/Year","Acad Year","Status"], tablefmt="grid"))
    else: print("📂 No re-exams.")
    conn.close()

def result_menu():
    while True:
        print("\n🎓 Result Menu:\n1. Add Result\n2. View Results\n3. Register Re-Exam\n4. View Re-Exam Status\n5. Go Back")
        choice = input("Choice (1-5): ").strip()
        if choice=="1": add_result()
        elif choice=="2": view_results()
        elif choice=="3": register_re_exam()
        elif choice=="4": view_re_exam_status()
        elif choice=="5": break
        else: print("❌ Invalid.")
