# attendance_management.py
import sqlite3
from database import connect_db

# ------------------- Mark Attendance -------------------
def mark_attendance():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()
    if not students:
        print("❌ No students found. Add students first.")
        conn.close()
        return

    date = input("Enter Date (YYYY-MM-DD): ")

    for sid, sname in students:
        status = input(f"{sname} (P/A): ").strip().upper()
        if status not in ["P", "A"]:
            status = "A"  # Default absent if invalid input
        cursor.execute(
            "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
            (sid, date, "Present" if status == "P" else "Absent")
        )

    conn.commit()
    print("✅ Attendance marked successfully.")
    conn.close()


# ------------------- View Attendance -------------------
def view_attendance():
    conn = connect_db()
    cursor = conn.cursor()

    date_filter = input("Enter Date (YYYY-MM-DD) to filter (or press Enter for all): ").strip()
    
    query = """
        SELECT students.name, attendance.date, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
    """
    params = ()

    if date_filter:
        query += " WHERE date = ?"
        params = (date_filter,)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    if rows:
        print("+----------------+------------+---------+")
        print("| Student        | Date       | Status  |")
        print("+----------------+------------+---------+")
        for r in rows:
            print(f"| {r[0]:<14} | {r[1]:<10} | {r[2]:<7} |")
        print("+----------------+------------+---------+")
    else:
        print("📂 No attendance records found.")

    conn.close()


# ------------------- Attendance Menu -------------------
def attendance_menu():
    while True:
        print("\n📅 Attendance Management Menu:")
        print("1. Mark Attendance")
        print("2. View Attendance")
        print("3. Go Back")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            mark_attendance()
        elif choice == "2":
            view_attendance()
        elif choice == "3":
            break
        else:
            print("❌ Invalid choice. Enter 1-3.")
# ------------------- End of attendance_management.py -------------------