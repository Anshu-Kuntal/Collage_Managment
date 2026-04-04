import sqlite3
from database import connect_db
from utils import input_float
from tabulate import tabulate


# ------------------- ADD TEACHER -------------------

def add_teacher():
    conn = connect_db()
    cursor = conn.cursor()

    name = input("Name: ").strip()
    emp_code = input("Emp Code: ").strip()
    subject = input("Subject: ").strip()
    salary = input_float("Salary: ")

    username = input("Set Username: ").strip()
    password = input("Set Password: ").strip()

    if not name or not emp_code:
        print("❌ Name and Emp Code required.")
        conn.close()
        return

    try:
        cursor.execute("""
            INSERT INTO teachers (name, emp_code, subject, salary, username, password)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, emp_code, subject, salary, username, password))

        conn.commit()
        print("✅ Teacher added successfully.")

    except sqlite3.IntegrityError as e:
        print("❌ Error:", e)

    conn.close()


# ------------------- VIEW TEACHERS -------------------

def view_teachers():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT emp_code, name, subject, salary, username
        FROM teachers
        ORDER BY emp_code ASC
    """)

    teachers = cursor.fetchall()

    if teachers:
        print(tabulate(
            teachers,
            headers=["Emp Code", "Name", "Subject", "Salary", "Username"],
            tablefmt="grid",
            stralign="left",
            numalign="right"
        ))
    else:
        print("📂 No records found.")

    conn.close()


# ------------------- UPDATE TEACHER -------------------

def update_teacher():
    conn = connect_db()
    cursor = conn.cursor()

    emp_code = input("Enter Emp Code: ").strip()

    cursor.execute("SELECT * FROM teachers WHERE emp_code=?", (emp_code,))
    t = cursor.fetchone()

    if not t:
        print("❌ Teacher not found.")
        conn.close()
        return

    name = input(f"Name ({t[1]}): ") or t[1]
    subject = input(f"Subject ({t[3]}): ") or t[3]

    salary_in = input(f"Salary ({t[4]}): ")
    salary = float(salary_in) if salary_in else t[4]

    username = input(f"Username ({t[5] if len(t) > 5 else ''}): ") or (t[5] if len(t) > 5 else "")
    password = input("New Password (leave blank to keep same): ") or (t[6] if len(t) > 6 else "")

    cursor.execute("""
        UPDATE teachers
        SET name=?, subject=?, salary=?, username=?, password=?
        WHERE emp_code=?
    """, (name, subject, salary, username, password, emp_code))

    conn.commit()
    conn.close()

    print("✅ Teacher updated successfully.")


# ------------------- DELETE TEACHER -------------------

def delete_teacher():
    conn = connect_db()
    cursor = conn.cursor()

    emp_code = input("Enter Emp Code: ").strip()

    confirm = input("Are you sure? (Y/N): ").strip().upper()

    if confirm != "Y":
        print("❌ Cancelled.")
        conn.close()
        return

    cursor.execute("DELETE FROM teachers WHERE emp_code=?", (emp_code,))
    conn.commit()

    print("✅ Deleted." if cursor.rowcount else "❌ Not found.")

    conn.close()


# ------------------- MENU -------------------

def teacher_menu():
    while True:
        print("\n👨‍🏫 ===== TEACHER MANAGEMENT =====")
        print("1. Add Teacher")
        print("2. View Teachers")
        print("3. Update Teacher")
        print("4. Delete Teacher")
        print("5. Go Back")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            add_teacher()
        elif choice == "2":
            view_teachers()
        elif choice == "3":
            update_teacher()
        elif choice == "4":
            delete_teacher()
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice.")