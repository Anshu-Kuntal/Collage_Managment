def predict_performance(marks_dict):
    total = sum(marks_dict.values())
    avg = total / len(marks_dict)

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

    result = "Pass" if avg >= 40 else "Fail"
    weak_subject = min(marks_dict, key=marks_dict.get)

    return avg, grade, result, weak_subject
