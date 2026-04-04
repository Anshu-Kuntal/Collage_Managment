import sqlite3
from database import connect_db
from utils import input_int
from tabulate import tabulate


# ------------------------------ Add Student ------------------------------
def add_student():
    conn = connect_db()
    cursor = conn.cursor()

    name = input("Name: ").strip()
    roll_no = input("Roll No: ").strip()
    father_name = input("Father Name: ").strip()
    mobile = input("Mobile No: ").strip()

    # Mobile validation
    if not mobile.isdigit() or len(mobile) != 10:
        print("❌ Invalid mobile number.")
        conn.close()
        return

    cursor.execute("SELECT id, course_name FROM courses ORDER BY id ASC")
    courses = cursor.fetchall()

    if not courses:
        print("❌ Add courses first.")
        conn.close()
        return

    print("\nCourses:")
    for cid, cname in courses:
        print(f"{cid}: {cname}")

    course_id = input_int("Course ID: ")
    year_or_sem = input_int("Year/Semester: ")

    # 🔥 SUBJECT FETCH
    cursor.execute("""
        SELECT subject_name, type
        FROM subjects
        WHERE course_id=? AND term_number=?
    """, (course_id, year_or_sem))

    subjects = cursor.fetchall()

    if not subjects:
        print("❌ No subjects found for this course/term.")
        conn.close()
        return

    # 🔥 Separate compulsory & optional
    compulsory = [s[0] for s in subjects if s[1] == "Compulsory"]
    optional = [s[0] for s in subjects if s[1] == "Optional"]

    # 🔥 Show compulsory
    print("\n📘 Compulsory Subjects:")
    for sub in compulsory:
        print(f"✔ {sub}")

    selected_optional = []

    # 🔥 Optional selection
    if optional:
        print("\n📗 Optional Subjects (choose):")
        for i, sub in enumerate(optional, 1):
            print(f"{i}. {sub}")

        choices = input("Enter choices (comma separated): ")

        for c in choices.split(","):
            try:
                selected_optional.append(optional[int(c.strip()) - 1])
            except:
                pass

    # 🔥 Final subjects
    final_subjects = compulsory + selected_optional

    print("\n✅ Final Subjects:")
    for sub in final_subjects:
        print(f"✔ {sub}")

    total_fees = input_int("Total Fees: ")
    fees_paid = input_int("Fees Paid: ")

    try:
        cursor.execute("""
            INSERT INTO students
            (name, roll_no, father_name, mobile, course_id, year_or_sem, total_fees, fees_paid)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, roll_no, father_name, mobile, course_id, year_or_sem, total_fees, fees_paid))

        # 🔥 Get student id
        student_id = cursor.lastrowid

        # 🔥 Save selected subjects
        for sub in final_subjects:
            cursor.execute("""
                INSERT INTO student_subjects (student_id, subject_name)
                VALUES (?, ?)
            """, (student_id, sub))

        conn.commit()
        print("✅ Student added successfully with subjects.")

    except sqlite3.IntegrityError as e:
        print("❌", e)

    conn.close()

# ------------------------------ View Students ------------------------------
def view_students():
    conn = connect_db()
    cursor = conn.cursor()

    search = input("Search (Name/Roll No or Enter): ").strip()

    query = """
        SELECT students.id,
               students.name,
               students.roll_no,
               students.father_name,
               students.mobile,
               courses.course_name,
               students.year_or_sem,
               students.total_fees,
               students.fees_paid
        FROM students
        LEFT JOIN courses ON students.course_id = courses.id
    """

    params = []

    if search:
        query += " WHERE students.name LIKE ? OR students.roll_no LIKE ?"
        params = [f"%{search}%", f"%{search}%"]

    query += " ORDER BY students.id ASC"

    cursor.execute(query, tuple(params))
    students = cursor.fetchall()

    if students:
        formatted = []
        for s in students:
            due = s[7] - s[8]
            status = "Paid" if due == 0 else "Due"

            formatted.append((*s, status))

        print(tabulate(
            formatted,
            headers=["ID","Name","Roll No","Father","Mobile","Course","Sem","Total","Paid","Status"],
            tablefmt="grid",
            stralign="left"
        ))
    else:
        print("📂 No records.")

    conn.close()


# ------------------------------ Update Student ------------------------------
def update_student():
    conn = connect_db()
    cursor = conn.cursor()

    roll_no = input("Roll No to update: ").strip()

    cursor.execute("SELECT * FROM students WHERE roll_no=?", (roll_no,))
    student = cursor.fetchone()

    if not student:
        print("❌ Not found.")
        conn.close()
        return

    name = input(f"Name ({student[1]}): ") or student[1]
    father = input(f"Father ({student[3]}): ") or student[3]
    mobile = input(f"Mobile ({student[4]}): ") or student[4]

    year_or_sem = input(f"Year/Sem ({student[6]}): ") or student[6]

    total_fees = input(f"Total Fees ({student[7]}): ")
    fees_paid = input(f"Fees Paid ({student[8]}): ")

    total_fees = int(total_fees) if total_fees else student[7]
    fees_paid = int(fees_paid) if fees_paid else student[8]

    cursor.execute("""
        UPDATE students
        SET name=?, father_name=?, mobile=?, year_or_sem=?, total_fees=?, fees_paid=?
        WHERE roll_no=?
    """, (name, father, mobile, year_or_sem, total_fees, fees_paid, roll_no))

    conn.commit()
    conn.close()

    print("✅ Updated successfully.")


# ------------------------------ Delete Student ------------------------------
def delete_student():
    conn = connect_db()
    cursor = conn.cursor()

    roll_no = input("Roll No to delete: ").strip()

    confirm = input("Are you sure? (Y/N): ").strip().upper()

    if confirm != "Y":
        print("❌ Cancelled.")
        conn.close()
        return

    cursor.execute("DELETE FROM students WHERE roll_no=?", (roll_no,))
    conn.commit()

    print("✅ Deleted." if cursor.rowcount else "❌ Not found.")

    conn.close()


# ------------------------------ Student Menu ------------------------------
def student_menu():
    while True:
        print("\n🎓 ===== STUDENT MANAGEMENT =====")
        print("1. Add Student")
        print("2. View / Search Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Go Back")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice.")