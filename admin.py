# admin.py
import sqlite3
import getpass
from database import connect_db

def create_admin_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    cursor.execute("SELECT * FROM admins")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", ("admin", "admin123"))
        conn.commit()
    conn.close()

def admin_login():
    conn = connect_db()
    cursor = conn.cursor()
    username = input("👤 Enter Admin Username: ")
    password = getpass.getpass("🔑 Enter Admin Password: ")
    cursor.execute("SELECT * FROM admins WHERE username=? AND password=?", (username, password))
    admin = cursor.fetchone()
    conn.close()
    if admin:
        print("✅ Login successful!")
        return True
    print("❌ Invalid credentials.")
    return False

def register_admin():
    conn = connect_db()
    cursor = conn.cursor()
    username = input("👤 New Admin Username: ")
    password = getpass.getpass("🔑 New Admin Password: ")
    try:
        cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("✅ Admin registered successfully.")
    except sqlite3.IntegrityError:
        print("❌ Username already exists.")
    conn.close()

def change_admin_password():
    conn = connect_db()
    cursor = conn.cursor()
    username = input("👤 Admin Username: ")
    old_pass = getpass.getpass("🔑 Old Password: ")
    cursor.execute("SELECT * FROM admins WHERE username=? AND password=?", (username, old_pass))
    if not cursor.fetchone():
        print("❌ Invalid username/password.")
        conn.close()
        return
    new_pass = getpass.getpass("🔑 New Password: ")
    cursor.execute("UPDATE admins SET password=? WHERE username=?", (new_pass, username))
    conn.commit()
    conn.close()
    print("✅ Password updated.")

def admin_settings_menu():
    while True:
        print("\n⚙️ Admin Settings:")
        print("1. Register Admin")
        print("2. Change Password")
        print("3. Go Back")
        choice = input("Enter choice (1-3): ").strip()
        if choice == "1": register_admin()
        elif choice == "2": change_admin_password()
        elif choice == "3": break
        else: print("❌ Invalid choice.")
