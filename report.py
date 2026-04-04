import os
from database import connect_db

# Folder to save report cards
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)


# ------------------- Grade System -------------------
def get_grade(percent):
    if percent >= 75:
        return "A"
    elif percent >= 60:
        return "B"
    elif percent >= 40:
        return "C"
    else:
        return "F"


# ------------------- Generate Single Report Card -------------------

def generate_report_card(student_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT students.name,
               students.roll_no,
               courses.course_name,
               students.year_or_sem
        FROM students
        JOIN courses ON students.course_id = courses.id
        WHERE students.id = ?
    """, (student_id,))

    student = cursor.fetchone()

    if not student:
        print("❌ Student not found.")
        conn.close()
        return

    name, roll_no, course, sem = student

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

    lines = []
    lines.append("🏫 COLLEGE MANAGEMENT SYSTEM")
    lines.append("📄 REPORT CARD")
    lines.append("=" * 50)

    lines.append(f"Name        : {name}")
    lines.append(f"Roll No     : {roll_no}")
    lines.append(f"Course      : {course}")
    lines.append(f"Semester    : {sem}")
    lines.append("-" * 50)

    lines.append(f"{'Subject':<20}{'Marks':<10}{'Max'}")

    total_marks = 0
    total_max = 0

    for subject, marks, max_marks in results:
        lines.append(f"{subject:<20}{marks:<10}{max_marks}")
        total_marks += marks
        total_max += max_marks

    percent = (total_marks / total_max * 100) if total_max else 0
    grade = get_grade(percent)
    status = "PASS" if percent >= 40 else "FAIL"

    lines.append("-" * 50)
    lines.append(f"Total Marks : {total_marks}/{total_max}")
    lines.append(f"Percentage  : {percent:.2f}%")
    lines.append(f"Grade       : {grade}")
    lines.append(f"Result      : {status}")
    lines.append("=" * 50)

    # 🔥 Clean filename
    safe_name = name.replace(" ", "_")
    report_path = os.path.join(REPORTS_DIR, f"{safe_name}_{roll_no}.txt")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    conn.close()

    print(f"✅ Report card saved to: {report_path}")


# ------------------- Generate All Reports -------------------

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

    conn.close()

    print("✅ All report cards generated successfully.")


# ------------------- Reports Menu -------------------

def reports_menu():
    while True:
        print("\n📝 Reports Menu:")
        print("1. Generate Report Card for a Student")
        print("2. Generate All Report Cards")
        print("3. Go Back")

        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            sid = input("Enter Student ID: ").strip()
            if sid.isdigit():
                generate_report_card(sid)
            else:
                print("❌ Invalid ID")

        elif choice == "2":
            generate_all_reports()

        elif choice == "3":
            break

        else:
            print("❌ Invalid choice.")
