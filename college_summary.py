# college_summary.py
from database import connect_db

# ------------------- College Summary -------------------
def college_summary():
    conn = connect_db()
    cursor = conn.cursor()

    print("\n🏫 College Summary\n")

    # ------------------- Courses -------------------
    print("📚 Courses Offered:")
    cursor.execute("SELECT id, course_name FROM courses ORDER BY course_name ASC")
    courses = cursor.fetchall()
    if courses:
        for cid, cname in courses:
            print(f"{cid}: {cname}")
    else:
        print("📂 No courses found.")

    # ------------------- Teachers Count -------------------
    cursor.execute("SELECT COUNT(*) FROM teachers")
    teacher_count = cursor.fetchone()[0]
    print(f"\n👩‍🏫 Total Teachers: {teacher_count}")

    # ------------------- Students Count -------------------
    cursor.execute("SELECT COUNT(*) FROM students")
    student_count = cursor.fetchone()[0]
    print(f"👨‍🎓 Total Students: {student_count}")

    # ------------------- Fees Summary -------------------
    print("\n💰 Fees Summary per Course:")
    cursor.execute("""
        SELECT c.id, c.course_name,
               SUM(s.total_fees) AS total_fees,
               SUM(s.fees_paid) AS fees_paid,
               SUM(s.total_fees - s.fees_paid) AS remaining_fees
        FROM students s
        JOIN courses c ON s.course_id = c.id
        GROUP BY c.id, c.course_name
        ORDER BY c.course_name ASC
    """)
    fee_rows = cursor.fetchall()
    if fee_rows:
        print("+-------------+---------------+--------------+-------------+------------------+")
        print("| Course ID   | Course Name   | Total Fees   | Fees Paid   | Remaining Fees   |")
        print("+-------------+---------------+--------------+-------------+------------------+")
        for r in fee_rows:
            print(f"| {r[0]:<11} | {r[1]:<13} | {r[2]:<12} | {r[3]:<11} | {r[4]:<16} |")
        print("+-------------+---------------+--------------+-------------+------------------+")
    else:
        print("📂 No fee records found.")

    # 🔥 ------------------- Fee Due Alert -------------------
    print("\n⚠ Fee Due Alert:")
    cursor.execute("""
        SELECT name, total_fees, fees_paid
        FROM students
    """)
    students = cursor.fetchall()

    found = False
    for name, total, paid in students:
        due = total - paid
        if due > 0:
            print(f"⚠ {name} → Due: {due}")
            found = True

    if not found:
        print("✅ All students have cleared fees")

    # ------------------- Average Results -------------------
    print("\n📊 Average Results per Course:")
    cursor.execute("""
        SELECT c.course_name, AVG(r.marks) as avg_marks
        FROM results r
        JOIN students s ON r.student_id = s.id
        JOIN courses c ON s.course_id = c.id
        GROUP BY c.course_name
        ORDER BY c.course_name ASC
    """)
    avg_results = cursor.fetchall()
    if avg_results:
        for course, avg in avg_results:
            print(f"{course}: {avg:.2f}")
    else:
        print("📂 No results found.")

    conn.close()

    # ------------------- Dashboard Summary -------------------
def dashboard_summary():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM teachers")
    teachers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM courses")
    courses = cursor.fetchone()[0]

    cursor.execute("""
        SELECT SUM(total_fees), SUM(fees_paid)
        FROM students
    """)
    total, paid = cursor.fetchone()

    total = total or 0
    paid = paid or 0

    print("\n📊 ===== DASHBOARD =====")
    print(f"👨‍🎓 Total Students: {students}")
    print(f"👨‍🏫 Total Teachers: {teachers}")
    print(f"📚 Total Courses: {courses}")
    print(f"💰 Total Fees: {total}")
    print(f"💵 Fees Collected: {paid}")
    print(f"⚠ Pending Fees: {total - paid}")

    conn.close()