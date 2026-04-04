import sqlite3
import getpass
from database import connect_db

from attendance_management import attendance_menu
from result_management import result_menu


# ------------------- UPDATE TABLE (RUN ONCE) -------------------

def update_teacher_table():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE teachers ADD COLUMN username TEXT")
        cursor.execute("ALTER TABLE teachers ADD COLUMN password TEXT")
        conn.commit()
        print("✅ Teacher login columns added")
    except:
        pass  # already exists

    conn.close()


# ------------------- SET LOGIN (ADMIN USE) -------------------

def set_teacher_login():
    conn = connect_db()
    cursor = conn.cursor()

    emp_code = input("Enter Teacher Emp Code: ").strip()

    cursor.execute("SELECT * FROM teachers WHERE emp_code=?", (emp_code,))
    teacher = cursor.fetchone()

    if not teacher:
        print("❌ Teacher not found")
        conn.close()
        return

    username = input("Set Username: ").strip()
    password = getpass.getpass("Set Password: ").strip()

    cursor.execute("""
        UPDATE teachers
        SET username=?, password=?
        WHERE emp_code=?
    """, (username, password, emp_code))

    conn.commit()
    conn.close()

    print("✅ Login credentials set successfully")


# ------------------- LOGIN -------------------

from database import connect_db

def teacher_login():
    conn = connect_db()
    cursor = conn.cursor()

    username = input("👨‍🏫 Enter Username: ").strip()
    password = input("🔑 Enter Password: ").strip()

    cursor.execute("""
        SELECT * FROM teachers
        WHERE username=? AND password=?
    """, (username, password))

    teacher = cursor.fetchone()
    conn.close()

    if teacher:
        print("✅ Teacher Login Successful!")
        return teacher
    else:
        print("❌ Invalid Username or Password")
        return None


# ------------------- DASHBOARD -------------------

def teacher_dashboard():
    while True:
        print("\n👨‍🏫 ===== TEACHER DASHBOARD =====")
        print(
            "1. Mark Attendance\n"
            "2. View Attendance\n"
            "3. Add Result\n"
            "4. View Result\n"
            "5. Logout"
        )

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            attendance_menu()

        elif choice == "2":
            attendance_menu()

        elif choice == "3":
            result_menu()

        elif choice == "4":
            result_menu()

        elif choice == "5":
            print("🔓 Logged out")
            break

        else:
            print("❌ Invalid choice")