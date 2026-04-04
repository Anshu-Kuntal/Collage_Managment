from database import connect_db
from tabulate import tabulate
from ai_module import predict_performance


def student_dashboard(student):
    student_id = student[0]

    while True:
        print("\n🎓 ===== STUDENT DASHBOARD =====")
        print("1. View Profile")
        print("2. View Attendance")
        print("3. View Results")
        print("4. Performance Analysis")
        print("5. Logout")

        choice = input("Enter choice (1-5): ").strip()

        conn = connect_db()
        cursor = conn.cursor()

        # ------------------- Profile -------------------
        if choice == "1":
            cursor.execute("""
                SELECT name, roll_no, father_name, mobile, year_or_sem
                FROM students WHERE id=?
            """, (student_id,))
            data = cursor.fetchone()

            print("\n👤 Profile:")
            print(data)

        # ------------------- Attendance -------------------
        elif choice == "2":
            cursor.execute("""
                SELECT date, subject, status
                FROM attendance
                WHERE student_id=?
            """, (student_id,))
            rows = cursor.fetchall()

            if rows:
                print(tabulate(rows, headers=["Date","Subject","Status"], tablefmt="grid"))
            else:
                print("📂 No attendance")

        # ------------------- Results -------------------
        elif choice == "3":
            cursor.execute("""
                SELECT subject, marks, max_marks
                FROM results
                WHERE student_id=?
            """, (student_id,))
            rows = cursor.fetchall()

            if rows:
                print(tabulate(rows, headers=["Subject","Marks","Max"], tablefmt="grid"))
            else:
                print("📂 No results")

        # ------------------- AI Performance -------------------
        elif choice == "4":
            cursor.execute("""
                SELECT subject, marks
                FROM results
                WHERE student_id=?
            """, (student_id,))
            data = cursor.fetchall()

            if not data:
                print("📂 No data")
            else:
                marks_dict = {sub: m for sub, m in data}
                avg, grade, result, weak = predict_performance(marks_dict)

                print("\n📊 Performance Analysis")
                print(f"Average: {avg}")
                print(f"Grade: {grade}")
                print(f"Result: {result}")
                print(f"Weak Subjects: {weak}")

        elif choice == "5":
            print("👋 Logout")
            break

        else:
            print("❌ Invalid choice")

        conn.close()