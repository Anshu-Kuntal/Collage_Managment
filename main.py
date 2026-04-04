from database import create_tables

from student_management import student_menu
from teacher_management import teacher_menu
from course_subject_management import course_subject_menu
from attendance_management import attendance_menu
from result_management import result_menu
from college_summary import college_summary, dashboard_summary
from report import reports_menu
from admin import admin_login, create_admin_table, admin_settings_menu

from teacher_auth import teacher_login
from teacher_dashboard import teacher_dashboard

from student_auth import student_login
from student_dashboard import student_dashboard


def admin_panel():
    while True:
        print("\n🏫 Admin Panel")
        print(
            "1. Student\n"
            "2. Teacher\n"
            "3. Course & Subject\n"
            "4. Result\n"
            "5. Attendance\n"
            "6. Dashboard\n"
            "7. College Summary\n"
            "8. Admin Settings\n"
            "9. Report Cards\n"
            "10. Logout"
        )

        choice = input("Choice (1-10): ").strip()

        if choice == "1":
            student_menu()
        elif choice == "2":
            teacher_menu()
        elif choice == "3":
            course_subject_menu()
        elif choice == "4":
            result_menu()
        elif choice == "5":
            attendance_menu()
        elif choice == "6":
            dashboard_summary()
        elif choice == "7":
            college_summary()
        elif choice == "8":
            admin_settings_menu()
        elif choice == "9":
            reports_menu()
        elif choice == "10":
            break
        else:
            print("❌ Invalid choice")


def main_menu():
    create_tables()
    create_admin_table()

    while True:
        print("\n🔐 Select Login Type")
        print("1. Admin Login")
        print("2. Teacher Login")
        print("3. Student Login")
        print("4. Exit")

        choice = input("Choice (1-4): ").strip()

        # ------------------- Admin -------------------
        if choice == "1":
            if admin_login():
                admin_panel()

        # ------------------- Teacher -------------------
        elif choice == "2":
            teacher = teacher_login()
            if teacher:
                teacher_dashboard(teacher)

        # ------------------- Student -------------------
        elif choice == "3":
            student = student_login()
            if student:
                student_dashboard(student)

        elif choice == "4":
            print("👋 Bye")
            break

        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main_menu()
