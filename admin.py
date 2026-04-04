import sqlite3
import getpass
from database import connect_db


# ------------------- CREATE TABLE -------------------

def create_admin_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT * FROM admins")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO admins (username, password) VALUES (?, ?)",
            ("admin", "admin123")
        )
    conn.commit()
    conn.close()


# ------------------- LOGIN -------------------

def admin_login():
    conn = connect_db()
    cursor = conn.cursor()

    username = input("👤 Enter Admin Username: ").strip()
    password = getpass.getpass("🔑 Enter Admin Password: ").strip()

    cursor.execute(
        "SELECT * FROM admins WHERE username=? AND password=?",
        (username, password)
    )

    admin = cursor.fetchone()
    conn.close()

    if admin:
        print("✅ Login successful!")
        return True

    print("❌ Invalid credentials.")
    return False


# ------------------- REGISTER ADMIN -------------------

def register_admin():
    conn = connect_db()
    cursor = conn.cursor()

    username = input("👤 New Admin Username: ").strip()
    password = getpass.getpass("🔑 New Admin Password: ").strip()

    if not username or not password:
        print("❌ Fields cannot be empty.")
        conn.close()
        return

    try:
        cursor.execute(
            "INSERT INTO admins (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        print("✅ Admin registered successfully.")

    except sqlite3.IntegrityError:
        print("❌ Username already exists.")

    conn.close()


# ------------------- CHANGE PASSWORD -------------------

def change_admin_password():
    conn = connect_db()
    cursor = conn.cursor()

    username = input("👤 Admin Username: ").strip()
    old_pass = getpass.getpass("🔑 Old Password: ").strip()

    cursor.execute(
        "SELECT * FROM admins WHERE username=? AND password=?",
        (username, old_pass)
    )

    if not cursor.fetchone():
        print("❌ Invalid username/password.")
        conn.close()
        return

    new_pass = getpass.getpass("🔑 New Password: ").strip()

    if not new_pass:
        print("❌ Password cannot be empty.")
        conn.close()
        return

    cursor.execute(
        "UPDATE admins SET password=? WHERE username=?",
        (new_pass, username)
    )

    conn.commit()
    conn.close()

    print("✅ Password updated successfully.")


# ------------------- ADMIN ACCOUNT SETTINGS -------------------

def admin_account_menu():
    while True:
        print("\n🔐 ===== ADMIN ACCOUNT SETTINGS =====")
        print("1. Register Admin")
        print("2. Change Password")
        print("3. Back")

        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            register_admin()
        elif choice == "2":
            change_admin_password()
        elif choice == "3":
            break
        else:
            print("❌ Invalid choice.")


# ------------------- ADMIN PANEL -------------------

def admin_settings_menu():
    while True:
        print("\n⚙️ ===== ADMIN PANEL =====")
        print("1. Admin Account Settings")
        print("2. Manage Courses")
        print("3. Manage Subjects")
        print("4. Assign Subjects to Semester")
        print("5. Back")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            admin_account_menu()

        elif choice == "2":
            print("👉 Use Course Management Module")

        elif choice == "3":
            print("👉 Use Subject Management Module")

        elif choice == "4":
            print("👉 Subject Assignment (Next Step)")

        elif choice == "5":
            break

        else:
            print("❌ Invalid choice.")