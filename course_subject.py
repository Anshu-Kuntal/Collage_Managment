from database import connect_db
from utils import input_int


# ------------------ COURSE ------------------

def add_course():
    conn = connect_db()
    cursor = conn.cursor()

    course_name = input("Course Name: ")
    duration = input_int("Duration (Years): ")

    while True:
        system_type = input("System Type (Year/Semester): ").strip().lower()
        if system_type in ("year", "semester"):
            system_type = system_type.capitalize()
            break
        print("❌ Enter only 'Year' or 'Semester'.")

    total_terms = input_int("Total Terms: ")

    cursor.execute("""
        INSERT INTO courses (course_name, duration_years, system_type, total_terms)
        VALUES (?, ?, ?, ?)
    """, (course_name, duration, system_type, total_terms))

    conn.commit()
    conn.close()
    print("✅ Course added.")


def view_courses():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, course_name, duration_years, system_type, total_terms
        FROM courses
        ORDER BY id ASC
    """)

    courses = cursor.fetchall()

    if courses:
        print("+--------+------------------------+------------+-------------+---------------+")
        print("| ID     | Name                   | Duration   | System      | TotalTerms   |")
        print("+--------+------------------------+------------+-------------+---------------+")

        for c in courses:
            print(
                f"| {c[0]:<6} | {c[1]:<22} | {c[2]:<10} | "
                f"{c[3]:<11} | {c[4]:<13} |"
            )

        print("+--------+------------------------+------------+-------------+---------------+")
    else:
        print("📂 No courses found.")

    conn.close()


def update_course():
    conn = connect_db()
    cursor = conn.cursor()

    cid = input_int("Enter Course ID to update: ")

    cursor.execute("SELECT * FROM courses WHERE id=?", (cid,))
    course = cursor.fetchone()

    if not course:
        print("❌ Course not found.")
        conn.close()
        return

    name = input(f"Course Name ({course[1]}): ") or course[1]

    duration_in = input(f"Duration Years ({course[2]}): ")
    duration = int(duration_in) if duration_in else course[2]

    while True:
        system_in = input(f"System Type ({course[3]}): ").strip()
        if not system_in:
            system = course[3]
            break
        if system_in.lower() in ("year", "semester"):
            system = system_in.capitalize()
            break
        print("❌ Enter only 'Year' or 'Semester'.")

    terms_in = input(f"Total Terms ({course[4]}): ")
    total_terms = int(terms_in) if terms_in else course[4]

    cursor.execute("""
        UPDATE courses
        SET course_name=?, duration_years=?, system_type=?, total_terms=?
        WHERE id=?
    """, (name, duration, system, total_terms, cid))

    conn.commit()
    conn.close()
    print("✅ Course updated.")


def delete_course():
    conn = connect_db()
    cursor = conn.cursor()

    cid = input_int("Enter Course ID to delete: ")

    cursor.execute("SELECT COUNT(*) FROM students WHERE course_id=?", (cid,))
    if cursor.fetchone()[0] > 0:
        print("❌ Cannot delete: students are enrolled in this course.")
        conn.close()
        return

    cursor.execute("DELETE FROM courses WHERE id=?", (cid,))
    conn.commit()

    print("✅ Course deleted." if cursor.rowcount else "❌ Course not found.")
    conn.close()


# ------------------ SUBJECT ------------------

def add_subject():
    conn = connect_db()
    cursor = conn.cursor()

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
    term_number = input_int("Term Number: ")
    subject_name = input("Subject Name: ").strip()

    # 🔥 NEW PART
    while True:
        sub_type = input("Type (C=Compulsory / O=Optional): ").strip().upper()
        if sub_type == "C":
            sub_type = "Compulsory"
            break
        elif sub_type == "O":
            sub_type = "Optional"
            break
        else:
            print("❌ Enter C or O")

    cursor.execute("""
        INSERT INTO subjects (course_id, term_number, subject_name, type)
        VALUES (?, ?, ?, ?)
    """, (course_id, term_number, subject_name, sub_type))

    conn.commit()
    conn.close()
    print("✅ Subject added.")

#------------------- VIEW SUBJECT ------------------
def view_subjects():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subjects.id,
               courses.course_name,
               subjects.term_number,
               subjects.subject_name,
               subjects.type
        FROM subjects
        JOIN courses ON subjects.course_id = courses.id
        ORDER BY subjects.id ASC
    """)

    subjects = cursor.fetchall()

    if subjects:
        print("+------+------------------------+------+------------------------+--------------+")
        print("| ID   | Course                 | Term | Subject                | Type         |")
        print("+------+------------------------+------+------------------------+--------------+")

        for s in subjects:
            print(
                f"| {s[0]:<4} | {s[1]:<22} | {s[2]:<4} | {s[3]:<22} | {s[4]:<12} |"
            )

        print("+------+------------------------+------+------------------------+--------------+")
    else:
        print("📂 No subjects found.")

    conn.close()

#------------------- UPDATE SUBJECT -------------------
def update_subject():
    conn = connect_db()
    cursor = conn.cursor()

    sid = input_int("Enter Subject ID to update: ")

    cursor.execute("SELECT * FROM subjects WHERE id=?", (sid,))
    sub = cursor.fetchone()

    if not sub:
        print("❌ Subject not found.")
        conn.close()
        return

    new_term = input(f"Term Number ({sub[2]}): ")
    term_number = int(new_term) if new_term else sub[2]

    new_name = input(f"Subject Name ({sub[3]}): ") or sub[3]

    cursor.execute("""
        UPDATE subjects
        SET term_number=?, subject_name=?
        WHERE id=?
    """, (term_number, new_name, sid))

    conn.commit()
    conn.close()
    print("✅ Subject updated.")

#------------------- DELETE SUBJECT -------------------
def delete_subject():
    conn = connect_db()
    cursor = conn.cursor()

    sid = input_int("Enter Subject ID to delete: ")

    cursor.execute("DELETE FROM subjects WHERE id=?", (sid,))
    conn.commit()

    print("✅ Subject deleted." if cursor.rowcount else "❌ Subject not found.")
    conn.close()


# ------------------ MENU ------------------

def course_subject_menu():
    while True:
        print("\n📘 Course & Subject Menu:")
        print("1. Add Course")
        print("2. View Courses")
        print("3. Update Course")
        print("4. Delete Course")
        print("5. Add Subject")
        print("6. View Subjects")
        print("7. Update Subject")
        print("8. Delete Subject")
        print("9. Go Back")

        choice = input("Choice (1-9): ").strip()

        if choice == "1":
            add_course()
        elif choice == "2":
            view_courses()
        elif choice == "3":
            update_course()
        elif choice == "4":
            delete_course()
        elif choice == "5":
            add_subject()
        elif choice == "6":
            view_subjects()
        elif choice == "7":
            update_subject()
        elif choice == "8":
            delete_subject()
        elif choice == "9":
            break
        else:
            print("❌ Invalid.")
