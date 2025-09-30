# database.py
import sqlite3

def connect_db():
    return sqlite3.connect("school.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Admins
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Courses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT UNIQUE NOT NULL,
            duration_years INTEGER NOT NULL,
            system_type TEXT CHECK(system_type IN ('Year', 'Semester')) NOT NULL,
            total_terms INTEGER NOT NULL
        )
    """)

    # Students
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            course_id INTEGER,
            year_or_sem TEXT,
            total_fees INTEGER DEFAULT 0,
            fees_paid INTEGER DEFAULT 0,
            FOREIGN KEY(course_id) REFERENCES courses(id)
        )
    """)

    # Teachers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            emp_code TEXT UNIQUE NOT NULL,
            subject TEXT NOT NULL,
            salary REAL
        )
    """)

    # Subjects
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            term_number INTEGER NOT NULL,
            subject_name TEXT NOT NULL,
            FOREIGN KEY(course_id) REFERENCES courses(id)
        )
    """)

    # Results
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            term_number INTEGER NOT NULL,
            academic_year TEXT NOT NULL,
            subject TEXT NOT NULL,
            marks INTEGER NOT NULL,
            max_marks INTEGER NOT NULL,
            is_reexam INTEGER DEFAULT 0,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)

    # Re-Exams
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS re_exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            term_number INTEGER NOT NULL,
            academic_year TEXT NOT NULL,
            status TEXT CHECK(status IN ('Pending', 'Completed')) NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)

    # Attendance
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            date TEXT NOT NULL,
            status TEXT CHECK(status IN ('Present', 'Absent')) NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)

    conn.commit()
    conn.close()
