def predict_performance(marks_dict):
    if not marks_dict:
        return 0, "N/A", "No Data", None

    total = sum(marks_dict.values())
    count = len(marks_dict)

    avg = total / count if count else 0
    avg = round(avg, 2)

    # 🔥 Grade system
    if avg >= 90:
        grade = "A+"
    elif avg >= 75:
        grade = "A"
    elif avg >= 60:
        grade = "B"
    elif avg >= 50:
        grade = "C"
    elif avg >= 40:
        grade = "D"
    else:
        grade = "F"

    # 🔥 Result
    result = "Pass" if avg >= 40 else "Fail"

    # 🔥 Weak subject (lowest marks)
    min_marks = min(marks_dict.values())
    weak_subjects = [sub for sub, m in marks_dict.items() if m == min_marks]

    return avg, grade, result, weak_subjects
