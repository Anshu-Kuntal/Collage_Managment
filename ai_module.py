# ai_module.py
from database import connect_db

def predict_student_performance(student_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Fetch all marks for student
    cursor.execute("SELECT marks, max_marks FROM results WHERE student_id=?", (student_id,))
    results = cursor.fetchall()
    
    if not results:
        print("📂 No results found for this student.")
        return
    
    total_marks = sum([r[0] for r in results])
    total_max = sum([r[1] for r in results])
    percentage = (total_marks / total_max) * 100
    
    print(f"📊 Predicted Performance for Student ID {student_id}: {percentage:.2f}%")
    
    if percentage >= 75:
        print("👍 Excellent! Keep up the good work.")
    elif percentage >= 50:
        print("👌 Average. Focus on weaker subjects.")
    else:
        print("⚠️ Needs improvement. Consider extra study or help sessions.")
    
    conn.close()

def recommend_courses():
    print("\n📚 Recommended Courses based on performance:")
    print("- Data Science / AI / ML for high performers")
    print("- Networking / Systems / Software for average performers")
    print("- Remedial or foundation courses for low performers")
