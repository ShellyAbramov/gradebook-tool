from student_gradebook import get_letter_grade
import models #necessary to access student, course, and student_course tables
from sqlalchemy.orm import Session 

def letter_grade_to_gpa(letter_grade):
    """Function to convert letter grade to GPA points."""
    grade_points ={
        "A+": 4.0,"A": 4.0,"A-": 3.7,
        "B+": 3.3,"B": 3.0,"B-": 2.7,
        "C+": 2.3,"C": 2.0,"C-": 1.7,
        "D+": 1.3,"D": 1.0,"D-": 0.7,
        "F+": 0.0, "F": 0.0, "F-": 0.0
    }
    return grade_points.get(letter_grade, 0.0)


def calculate_gpa(student_id_number: str, db: Session):
    """Function to calculate GPA"""
    student = db.query(models.Student).filter(models.Student.student_id_number == student_id_number).first()
    if not student:
        return 0.0
    
    student_courses = db.query(models.StudentCourse).filter(models.StudentCourse.student_id == student.id).join(models.Course).all()
    if not student_courses:
        return 0.0
    

    total_gpa_points = 0.0
    total_credits = 0

    for sc in student_courses:

        credits = sc.course.credits

        letter_grade = get_letter_grade(sc.grade)

        gpa_points = letter_grade_to_gpa(letter_grade)

        weighted_points = gpa_points * credits

        total_gpa_points += weighted_points
        total_credits += credits

    if total_credits == 0:
        return 0.0

    overall_gpa = total_gpa_points / total_credits
    return round(overall_gpa, 2) 

def student_gpa_in_records(student_id_number: str, db: Session):
    """Function to get the GPA of a student and put it into the table/db.(Always returns a float)"""
    student = db.query(models.Student).filter(models.Student.student_id_number == student_id_number).first()
    if not student:
        return {"error": "Student not found."}
    
    # Calculate GPA using the calculate_gpa function
    gpa = calculate_gpa(student.student_id_number, db)

    #update GPA in student info table
    student.GPA = gpa if isinstance(gpa, float) else 0.0
    db.commit()

#for testing purposes
    return {
        "message": f"GPA for {student.name} with ID {student.student_id_number} is {gpa}."
    }


