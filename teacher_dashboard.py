from attendance_management import mark_attendance, view_attendance
from result_management import add_result, view_results


def teacher_dashboard(teacher):
    while True:
        print("\n👨‍🏫 ===== TEACHER DASHBOARD =====")
        print("1. Mark Attendance")
        print("2. View Attendance")
        print("3. Add Result")
        print("4. View Results")
        print("5. Logout")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            mark_attendance()

        elif choice == "2":
            view_attendance()

        elif choice == "3":
            add_result()

        elif choice == "4":
            view_results()

        elif choice == "5":
            print("👋 Logout successful")
            break

        else:
            print("❌ Invalid choice")