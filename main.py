from database import create_tables

from student_management import student_menu
from teacher_management import teacher_menu
from course_subject_management import course_subject_menu
from attendance_management import attendance_menu
from result_management import result_menu
from college_summary import college_summary
from reports import reports_menu
from admin import admin_login, create_admin_table, admin_settings_menu
from ai_module import predict_performance


def main_menu():
    create_tables()
    create_admin_table()

    print("🔐 Login required")
    if not admin_login():
        print("⛔ Exiting.")
        return

    while True:
        print("\n🏫 College Management System")
        print(
            "1. Student\n"
            "2. Teacher\n"
            "3. Course & Subject\n"
            "4. Result\n"
            "5. Attendance\n"
            "6. Summary\n"
            "7. Admin\n"
            "8. Report Cards\n"
            "9. Exit"
        )

        choice = input("Choice (1-9): ").strip()

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
            college_summary()
        elif choice == "7":
            admin_settings_menu()
        elif choice == "8":
            reports_menu()
        elif choice == "9":
            print("👋 Bye")
            break
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    main_menu()
