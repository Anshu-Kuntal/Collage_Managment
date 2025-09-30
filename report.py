# reports.py
import os
from database import connect_db
from tabulate import tabulate

# Folder to save report cards
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)


# ------------------- Generate Report Card -------------------
def generate_report_card(student_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Get student info
    cursor.execute("""
        SELECT students.name, students.roll_no, courses.course_name
        FROM students
        JOIN courses ON students.course_id = courses.id
        WHERE students.id = ?
    """, (student_id,))
    student = cursor.fetchone()
    if not student:
        print("❌ Student not found.")
        conn.close()
        return

    name, roll_no, course = student

    # Get student results
    cursor.execute("""
        SELECT subject, marks, max_marks
        FROM results
        WHERE student_id = ?
    """, (student_id,))
    results = cursor.fetchall()

    if not results:
        print("❌ No results found for this student.")
        conn.close()
        return

    # Prepare report content
    report_lines = [
        f"🏫 College Management System - Report Card",
        f"Student Name : {name}",
        f"Roll Number  : {roll_no}",
        f"Course       : {course}",
        "-"*40,
        f"{'Subject':<20} {'Marks':<5} {'Max Marks':<9}"
    ]

    total_marks = 0
    total_max = 0
    for subject, marks, max_marks in results:
        report_lines.append(f"{subject:<20} {marks:<5} {max_marks:<9}")
        total_marks += marks
        total_max += max_marks

    percentage = (total_marks / total_max * 100) if total_max else 0
    report_lines.append("-"*40)
    report_lines.append(f"Total Marks  : {total_marks}/{total_max}")
    report_lines.append(f"Percentage   : {percentage:.2f}%")

    # Save to file
    report_file = os.path.join(REPORTS_DIR, f"{roll_no}_report.txt")
    with open(report_file, "w") as f:
        f.write("\n".join(report_lines))

    print(f"✅ Report card generated: {report_file}")
    conn.close()


# ------------------- Generate All Report Cards -------------------
def generate_all_reports():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students")
    students = cursor.fetchall()
    if not students:
        print("❌ No students found.")
        conn.close()
        return

    for (sid,) in students:
        generate_report_card(sid)

    print("✅ All report cards generated successfully.")
    conn.close()


# ------------------- Reports Menu -------------------
def reports_menu():
    while True:
        print("\n📝 Reports Menu:")
        print("1. Generate Report Card for a Student")
        print("2. Generate All Report Cards")
        print("3. Go Back")

        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            student_id = input("Enter Student ID: ")
            generate_report_card(student_id)
        elif choice == "2":
            generate_all_reports()
        elif choice == "3":
            break
        else:
            print("❌ Invalid input. Enter 1-3.")
