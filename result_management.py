# result_management.py
import sqlite3
from database import connect_db
from tabulate import tabulate

#------------------- Add Result -------------------
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

#------------------- View Results -------------------
def view_results():
    conn = connect_db()
    cursor = conn.cursor()

    student_id = input("Student ID (or Enter all): ").strip()
    course_id = input("Course ID (or Enter): ").strip()
    year_sem = input("Year/Sem (or Enter): ").strip()
    academic_year = input("Academic Year (or Enter): ").strip()

    subject = ""

    # 🔥 Subject dropdown (safe + validated)
    if course_id and year_sem:
        cursor.execute("""
            SELECT DISTINCT subject_name
            FROM student_subjects ss
            JOIN students s ON ss.student_id = s.id
            WHERE s.course_id=? AND s.year_or_sem=?
        """, (course_id, year_sem))

        subjects = cursor.fetchall()

        if subjects:
            print("\n📘 Available Subjects:")
            for i, sub in enumerate(subjects, 1):
                print(f"{i}. {sub[0]}")

            choice = input("Select subject (or Enter to skip): ").strip()

            if choice:
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(subjects):
                        subject = subjects[index][0]
                    else:
                        print("❌ Invalid selection, skipping subject filter.")
                except:
                    print("❌ Invalid input, skipping subject filter.")

    query = """
        SELECT students.name,
               courses.course_name,
               students.year_or_sem,
               results.academic_year,
               results.subject,
               results.marks,
               results.max_marks
        FROM results
        JOIN students ON results.student_id = students.id
        JOIN courses ON students.course_id = courses.id
    """

    conditions = []
    params = []

    if student_id:
        conditions.append("students.id=?")
        params.append(student_id)

    if course_id:
        conditions.append("students.course_id=?")
        params.append(course_id)

    if year_sem:
        conditions.append("students.year_or_sem=?")
        params.append(year_sem)

    if subject:
        conditions.append("results.subject=?")
        params.append(subject)

    if academic_year:
        conditions.append("results.academic_year=?")
        params.append(academic_year)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY students.name ASC"

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()

    if rows:
        print(tabulate(
            rows,
            headers=["Student", "Course", "Sem", "Academic Year", "Subject", "Marks", "Max Marks"],
            tablefmt="grid",
            stralign="left"
        ))
    else:
        print("📂 No results found.")

    conn.close()

#------------------- Register Re-Exam -------------------
def register_re_exam():
    conn = connect_db(); cursor = conn.cursor()
    student_id = input("Student ID: "); subject=input("Subject: ")
    term_number = input("Term/Year: "); academic_year = input("Academic Year: ")
    cursor.execute("INSERT INTO re_exams (student_id, subject, term_number, academic_year, status) VALUES (?, ?, ?, ?, 'Pending')",
                   (student_id, subject, term_number, academic_year))
    conn.commit(); print("✅ Re-Exam registered."); conn.close()


#------------------- Register Re-Exam -------------------
def register_re_exam():
    conn = connect_db()
    cursor = conn.cursor()

    student_id = input("Student ID: ").strip()

    # 🔥 Validate student
    cursor.execute("SELECT year_or_sem FROM students WHERE id=?", (student_id,))
    info = cursor.fetchone()

    if not info:
        print("❌ Student not found.")
        conn.close()
        return

    term_number = info[0]

    # 🔥 Fetch only selected subjects
    cursor.execute("""
        SELECT subject_name
        FROM student_subjects
        WHERE student_id=?
    """, (student_id,))

    subjects = cursor.fetchall()

    if not subjects:
        print("❌ No subjects assigned to this student.")
        conn.close()
        return

    print("\n📘 Subjects:")
    for i, sub in enumerate(subjects, 1):
        print(f"{i}. {sub[0]}")

    # 🔥 Select subject safely
    try:
        choice = int(input("Select subject: "))
        subject = subjects[choice - 1][0]
    except:
        print("❌ Invalid subject selection")
        conn.close()
        return

    academic_year = input("Academic Year: ").strip()

    cursor.execute("""
        INSERT INTO re_exams (student_id, subject, term_number, academic_year, status)
        VALUES (?, ?, ?, ?, 'Pending')
    """, (student_id, subject, term_number, academic_year))

    conn.commit()
    conn.close()

    print("✅ Re-Exam registered successfully.")


#------------------- View Re-Exam Status -------------------
def view_re_exam_status():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT re_exams.id,
               students.name,
               re_exams.subject,
               re_exams.term_number,
               re_exams.academic_year,
               re_exams.status
        FROM re_exams
        JOIN students ON re_exams.student_id = students.id
        ORDER BY re_exams.id ASC
    """)

    rows = cursor.fetchall()

    if rows:
        print(tabulate(
            rows,
            headers=["ID","Student","Subject","Term","Academic Year","Status"],
            tablefmt="grid",
            stralign="left"
        ))
    else:
        print("📂 No re-exams found.")

    conn.close()


#-------------------- AI Prediction Function -------------------
def ai_prediction():
    print("\n🤖 AI Performance Analysis")

    conn = connect_db()
    cursor = conn.cursor()

    student_id = input("Enter Student ID: ")

    cursor.execute("""
        SELECT subject, marks, max_marks
        FROM results
        WHERE student_id=?
    """, (student_id,))

    data = cursor.fetchall()

    if not data:
        print("❌ No data found for this student.")
        conn.close()
        return

    marks_dict = {}
    total = 0
    count = 0

    for subject, marks, max_marks in data:
        percentage = (marks / max_marks) * 100
        marks_dict[subject] = percentage
        total += percentage
        count += 1

    avg = total / count

    # Grade logic
    if avg >= 90:
        grade = "A+"
    elif avg >= 75:
        grade = "A"
    elif avg >= 60:
        grade = "B"
    elif avg >= 50:
        grade = "C"
    elif avg >= 40:
        grade = "D"
    else:
        grade = "F"

    result = "Pass" if avg >= 40 else "Fail"
    weak_subject = min(marks_dict, key=marks_dict.get)

    print("\n--- AI Result ---")
    print("Average %:", round(avg, 2))
    print("Grade:", grade)
    print("Result:", result)
    print("Weak Subject:", weak_subject)

    conn.close()


def result_menu():
    while True:
        print("\n🎓 Result Menu:\n1. Add Result\n2. View Results\n3. Register Re-Exam\n4. View Re-Exam Status\n5. AI Performance Analysis\n6. Go Back")
        
        choice = input("Choice (1-6): ").strip()
        
        if choice=="1": 
            add_result()
        elif choice=="2": 
            view_results()
        elif choice=="3": 
            register_re_exam()
        elif choice=="4": 
            view_re_exam_status()
        elif choice=="5": 
            ai_prediction()   
        elif choice=="6": 
            break
        else: 
            print("❌ Invalid.")
