# teacher_management.py
import sqlite3
from database import connect_db
from utils import input_int, input_float

def add_teacher():
    conn = connect_db(); cursor = conn.cursor()
    name = input("Name: ")
    emp_code = input("Emp Code: ")
    subject = input("Subject: ")
    salary = input_float("Salary: ")
    try:
        cursor.execute("INSERT INTO teachers (name, emp_code, subject, salary) VALUES (?, ?, ?, ?)",
                       (name, emp_code, subject, salary))
        conn.commit(); print("✅ Added.")
    except sqlite3.IntegrityError as e: print("❌", e)
    conn.close()

def view_teachers():
    conn = connect_db(); cursor = conn.cursor()
    cursor.execute("SELECT emp_code, name, subject, salary FROM teachers"); teachers = cursor.fetchall()
    if teachers:
        print("+------------+----------------+----------------+------------+")
        print("| Emp Code   | Name           | Subject        | Salary     |")
        print("+------------+----------------+----------------+------------+")
        for t in teachers: print(f"| {t[0]:<10} | {t[1]:<14} | {t[2]:<14} | {t[3]:<10} |")
        print("+------------+----------------+----------------+------------+")
    else: print("📂 No records.")
    conn.close()

def update_teacher():
    conn = connect_db(); cursor = conn.cursor(); emp_code=input("Emp Code: ")
    cursor.execute("SELECT * FROM teachers WHERE emp_code=?", (emp_code,))
    t=cursor.fetchone(); 
    if not t: print("❌ Not found."); conn.close(); return
    name=input(f"Name ({t[1]}): ") or t[1]; subject=input(f"Subject ({t[3]}): ") or t[3]; salary=input(f"Salary ({t[4]}): ") or t[4]
    cursor.execute("UPDATE teachers SET name=?, subject=?, salary=? WHERE emp_code=?", (name, subject, salary, emp_code))
    conn.commit(); print("✅ Updated."); conn.close()

def delete_teacher():
    conn = connect_db(); cursor = conn.cursor(); emp_code=input("Emp Code: ")
    cursor.execute("DELETE FROM teachers WHERE emp_code=?", (emp_code,))
    conn.commit(); print("✅ Deleted." if cursor.rowcount else "❌ Not found."); conn.close()

def teacher_menu():
    while True:
        print("\n👨‍🏫 Teacher Menu:\n1. Add\n2. View\n3. Update\n4. Delete\n5. Go Back")
        choice=input("Choice (1-5): ").strip()
        if choice=="1": add_teacher()
        elif choice=="2": view_teachers()
        elif choice=="3": update_teacher()
        elif choice=="4": delete_teacher()
        elif choice=="5": break
        else: print("❌ Invalid.")
