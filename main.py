# main.py
from student import student_menu
from teacher import teacher_menu
from course_subject import course_subject_menu
from result_management import result_menu
from attendance import attendance_menu
from admin import admin_login, create_admin_table, admin_settings_menu
from college_summary import college_summary
from report import reports_menu

def main_menu():
    create_admin_table()
    print("🔐 Login required")
    if not admin_login(): print("⛔ Exiting."); return
    while True:
        print("\n🏫 College Management System")
        print("1. Student\n2. Teacher\n3. Course & Subject\n4. Result\n5. Attendance\n6. Summary\n7. Admin\n8. Report Cards\n9. Exit")
        choice = input("Choice (1-8): ").strip()
        if choice=="1": 
            student_menu()
        elif choice=="2": 
            teacher_menu()
        elif choice=="3":
            course_subject_menu()
        elif choice=="4":
            result_menu()
        elif choice=="5":
            attendance_menu()
        elif choice=="6": 
            college_summary()
        elif choice=="7":
            admin_settings_menu()
        elif choice == "8":
            reports_menu()
        elif choice=="9": 
            print("👋 Bye"); break
        else: print("❌ Invalid.")
        
if __name__=="__main__":
    main_menu()
