from database import connect_db
from tabulate import tabulate


# ------------------- Mark Attendance -------------------
def mark_attendance():
    conn = connect_db()
    cursor = conn.cursor()

    course_id = input("Enter Course ID: ").strip()
    year_sem = input("Enter Year/Sem: ").strip()
    date = input("Enter Date (YYYY-MM-DD): ").strip()

    # Validation
    if not course_id or not year_sem or not date:
        print("❌ All fields are required!")
        conn.close()
        return

    cursor.execute("""
        SELECT id, name FROM students
        WHERE course_id=? AND year_or_sem=?
        ORDER BY id ASC
    """, (course_id, year_sem))

    students = cursor.fetchall()

    if not students:
        print("❌ No students found.")
        conn.close()
        return

    for sid, sname in students:

        # 🔥 Fetch subjects for this student
        cursor.execute("""
            SELECT subject_name
            FROM student_subjects
            WHERE student_id=?
        """, (sid,))

        subjects = cursor.fetchall()

        if not subjects:
            print(f"❌ No subjects found for {sname}")
            continue

        print(f"\n📘 Subjects for {sname}:")
        for i, sub in enumerate(subjects, 1):
            print(f"{i}. {sub[0]}")

        # 🔥 Select subject
        try:
            choice = int(input("Select subject number: "))
            subject = subjects[choice - 1][0]
        except:
            print("❌ Invalid subject selection")
            continue

        # 🔥 Attendance input
        while True:
            status = input(f"{sname} (P/A): ").strip().upper()
            if status in ("P", "A"):
                break
            else:
                print("❌ Enter only P or A")

        final_status = "Present" if status == "P" else "Absent"

        cursor.execute("""
            INSERT INTO attendance (student_id, date, subject, status)
            VALUES (?, ?, ?, ?)
        """, (sid, date, subject, final_status))

    conn.commit()
    conn.close()

    print("✅ Attendance marked successfully.")

# ------------------- View Attendance -------------------

def view_attendance():
    conn = connect_db()
    cursor = conn.cursor()

    course_id = input("Course ID (or Enter): ").strip()
    year_sem = input("Year/Sem (or Enter): ").strip()
    date = input("Date (YYYY-MM-DD or Enter): ").strip()

    # 🔥 Subject dropdown system
    subject = ""

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

            try:
                choice = input("Select subject (or Enter to skip): ").strip()
                if choice:
                    subject = subjects[int(choice) - 1][0]
            except:
                print("❌ Invalid subject selection")

    query = """
        SELECT students.name,
               courses.course_name,
               students.year_or_sem,
               attendance.subject,
               attendance.date,
               attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        JOIN courses ON students.course_id = courses.id
    """

    conditions = []
    params = []

    if course_id:
        conditions.append("students.course_id=?")
        params.append(course_id)

    if year_sem:
        conditions.append("students.year_or_sem=?")
        params.append(year_sem)

    if subject:
        conditions.append("attendance.subject=?")
        params.append(subject)

    if date:
        conditions.append("attendance.date=?")
        params.append(date)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY attendance.date ASC"

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()

    if rows:
        print(tabulate(
            rows,
            headers=["Name", "Course", "Sem", "Subject", "Date", "Status"],
            tablefmt="grid",
            stralign="left"
        ))
    else:
        print("📂 No records found.")

    conn.close()

#-------------------- Update Attendance -------------------
def update_attendance():
    conn = connect_db()
    cursor = conn.cursor()

    date = input("Enter Date (YYYY-MM-DD): ").strip()

    cursor.execute("""
        SELECT attendance.id, students.name, attendance.subject, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        WHERE attendance.date=?
    """, (date,))

    rows = cursor.fetchall()

    if not rows:
        print("❌ No records found for this date.")
        conn.close()
        return

    print("\n📋 Attendance Records:")
    print(tabulate(rows, headers=["ID", "Name", "Subject", "Status"], tablefmt="grid"))

    att_id = input("Enter Attendance ID to update: ").strip()

    new_status = input("Enter new status (P/A): ").strip().upper()

    if new_status not in ("P", "A"):
        print("❌ Invalid input.")
        conn.close()
        return

    final_status = "Present" if new_status == "P" else "Absent"

    cursor.execute("""
        UPDATE attendance
        SET status=?
        WHERE id=?
    """, (final_status, att_id))

    conn.commit()
    conn.close()

    print("✅ Attendance updated successfully.")

#-------------------- Delete Attendance -------------------
def delete_attendance():
    conn = connect_db()
    cursor = conn.cursor()

    date = input("Enter Date (YYYY-MM-DD): ").strip()

    cursor.execute("""
        SELECT attendance.id, students.name, attendance.subject, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        WHERE attendance.date=?
    """, (date,))

    rows = cursor.fetchall()

    if not rows:
        print("❌ No records found.")
        conn.close()
        return

    print("\n📋 Attendance Records:")
    print(tabulate(rows, headers=["ID", "Name", "Subject", "Status"], tablefmt="grid"))

    att_id = input("Enter Attendance ID to delete: ").strip()

    confirm = input("Are you sure? (Y/N): ").strip().upper()

    if confirm != "Y":
        print("❌ Cancelled.")
        conn.close()
        return

    cursor.execute("DELETE FROM attendance WHERE id=?", (att_id,))

    conn.commit()
    conn.close()

    print("🗑️ Attendance deleted successfully.")


# ------------------- Attendance Report -------------------

def attendance_report():
    conn = connect_db()
    cursor = conn.cursor()

    print("\n📊 Generate Attendance Report")

    course_id = input("Course ID (or Enter): ").strip()
    year_sem = input("Year/Sem (or Enter): ").strip()

    subject = ""

    # 🔥 Subject dropdown (only valid subjects)
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
               SUM(CASE WHEN attendance.status='Present' THEN 1 ELSE 0 END),
               COUNT(attendance.id)
        FROM attendance
        JOIN students ON attendance.student_id = students.id
    """

    conditions = []
    params = []

    if course_id:
        conditions.append("students.course_id=?")
        params.append(course_id)

    if year_sem:
        conditions.append("students.year_or_sem=?")
        params.append(year_sem)

    if subject:
        conditions.append("attendance.subject=?")
        params.append(subject)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " GROUP BY students.id ORDER BY students.name ASC"

    cursor.execute(query, tuple(params))
    data = cursor.fetchall()

    if not data:
        print("📂 No attendance data.")
        conn.close()
        return

    report = []

    for name, present, total in data:
        percent = (present / total) * 100 if total else 0
        status = "Defaulter ⚠" if percent < 75 else "OK"

        report.append((name, present, total, f"{percent:.2f}%", status))

    print(tabulate(
        report,
        headers=["Name", "Present", "Total", "%", "Status"],
        tablefmt="grid",
        stralign="left"
    ))

    conn.close()


# ------------------- Menu -------------------

def attendance_menu():
    while True:
        print("\n📅 Attendance Management Menu:")
        print("1. Mark Attendance")
        print("2. View Attendance")
        print("3. Attendance Report")
        print("4. Update Attendance")
        print("5. Delete Attendance")
        print("6. Go Back")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            mark_attendance()
        elif choice == "2":
            view_attendance()
        elif choice == "3":
            attendance_report()
        elif choice == "4":
            update_attendance()
        elif choice == "5":
            delete_attendance()
        elif choice == "6":
            break
        else:
            print("❌ Invalid choice.")