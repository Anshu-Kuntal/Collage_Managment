# course_subject_management.py
import sqlite3
from database import connect_db
from utils import input_int

def add_course():
    conn = connect_db(); cursor = conn.cursor()
    course_name = input("Course Name: ")
    duration = input_int("Duration (Years): ")
    system_type = input("System Type (Year/Semester): ").strip().capitalize()
    total_terms = input_int("Total Terms: ")
    cursor.execute("INSERT INTO courses (course_name, duration_years, system_type, total_terms) VALUES (?, ?, ?, ?)",
                   (course_name, duration, system_type, total_terms))
    conn.commit(); print("✅ Course added."); conn.close()

def view_courses():
    conn = connect_db(); cursor = conn.cursor()
    cursor.execute("SELECT id, course_name, duration_years, system_type, total_terms FROM courses ORDER BY course_name ASC")
    courses = cursor.fetchall()
    if courses:
        print("+----+----------------+----------+--------+------------+")
        print("| ID | Name           | Duration | System | TotalTerms |")
        print("+----+----------------+----------+--------+------------+")
        for c in courses: print(f"| {c[0]:<2} | {c[1]:<14} | {c[2]:<8} | {c[3]:<6} | {c[4]:<10} |")
        print("+----+----------------+----------+--------+------------+")
    else: print("📂 No courses found.")
    conn.close()

def add_subject():
    conn = connect_db(); cursor = conn.cursor()
    cursor.execute("SELECT id, course_name FROM courses ORDER BY course_name ASC")
    courses = cursor.fetchall()
    if not courses: print("❌ Add courses first."); conn.close(); return
    print("\nCourses:"); 
    for cid, cname in courses: print(f"{cid}: {cname}")
    course_id = input_int("Course ID: ")
    term_number = input_int("Term Number: ")
    subject_name = input("Subject Name: ")
    cursor.execute("INSERT INTO subjects (course_id, term_number, subject_name) VALUES (?, ?, ?)",
                   (course_id, term_number, subject_name))
    conn.commit(); print("✅ Subject added."); conn.close()

def view_subjects():
    conn = connect_db(); cursor = conn.cursor()
    cursor.execute("""
        SELECT subjects.id, courses.course_name, subjects.term_number, subjects.subject_name
        FROM subjects
        JOIN courses ON subjects.course_id=courses.id
        ORDER BY courses.course_name ASC, subjects.term_number ASC
    """)
    subjects = cursor.fetchall()
    if subjects:
        print("+----+----------------+------+----------------+")
        print("| ID | Course          |Term  | Subject        |")
        print("+----+----------------+------+----------------+")
        for s in subjects: print(f"| {s[0]:<2} | {s[1]:<14} | {s[2]:<4} | {s[3]:<14} |")
        print("+----+----------------+------+----------------+")
    else: print("📂 No subjects found.")
    conn.close()

def course_subject_menu():
    while True:
        print("\n📘 Course & Subject Menu:")
        print("1. Add Course\n2. View Courses\n3. Add Subject\n4. View Subjects\n5. Go Back")
        choice = input("Choice (1-5): ").strip()
        if choice=="1": add_course()
        elif choice=="2": view_courses()
        elif choice=="3": add_subject()
        elif choice=="4": view_subjects()
        elif choice=="5": break
        else: print("❌ Invalid.")
