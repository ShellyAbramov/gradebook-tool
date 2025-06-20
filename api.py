from fastapi import FastAPI, HTTPException, Depends
from  pydantic import BaseModel
from typing import Annotated, List
#from student_gradebook_api import add_student_info, calculate_stats_from_file
from student_gradebook import get_letter_grade  # Importing the function to get letter grades
#student_info, student_letter_grades, student_gradebook_stats, calculate_stats_from_file
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date


app = FastAPI()
models.Base.metadata.create_all(bind=engine)  # Create tables in the database


def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#create some annotations
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Student Gradebook API"} #for testing purposes


class StudentInfo(BaseModel):
    """Pydantic model for student information."""
    name: str
    birthdate: date 
    school_name: str
    major: str
    graduation_year: int
    student_id_number: str  

@app.post("/add_student_info") #API makes a connection to the database here as well
async def add_student(student: StudentInfo, db: db_dependency):
    """Endpoint to add a student's information."""
    
    db_student = models.Student(name=student.name, birthdate=student.birthdate,
                                school_name=student.school_name, major=student.major, graduation_year=student.graduation_year, student_id_number=student.student_id_number)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return {"message": f"Student {student.name} added successfully."}


@app.put("/update_school_name/{student_id}")
async def update_school_name(student_id: int, school_name: str, db: db_dependency):
    """Endpoint to update a student's school name."""
    """Update a student's school name by their ID."""
    result = db.query(models.Student).filter(models.Student.id == student_id).first() 
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student = result
    db_student.school_name = school_name
    db.commit()
    db.refresh(db_student)
    return {"message": f"Student {db_student.name}'s school name updated successfully."}

@app.put("/update_major/{student_id}")
async def update_major(student_id: int, major: str, db: db_dependency):
    """Endpoint to update a student's major."""
    """Update a student's major by their ID."""
    result = db.query(models.Student).filter(models.Student.id == student_id).first() 
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student = result
    db_student.major = major
    db.commit()
    db.refresh(db_student)
    return {"message": f"Student {db_student.name}'s major updated successfully."}

@app.put("/update_grad_year/{student_id}")
async def update_grad_year(student_id: int, graduation_year: int, db: db_dependency):
    """Endpoint to update a student's graduation year."""
    """Update a student's graduation year by their ID."""
    result = db.query(models.Student).filter(models.Student.id == student_id).first() 
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student = result
    db_student.graduation_year = graduation_year
    db.commit()
    db.refresh(db_student)
    return {"message": f"Student {db_student.name}'s graduation year updated successfully."}

@app.get("/student_info")
async def get_student_info(db: db_dependency) -> List[StudentInfo]:
    """Endpoint to retrieve all students' information."""
    """Get all students from the database."""
    students = db.query(models.Student).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return [StudentInfo(name=student.name, birthdate=student.birthdate, school_name=student.school_name,
                        major=student.major, graduation_year=student.graduation_year) for student in students]

@app.get("/student_info/{student_id}")
async def get_student_info_by_id(student_id: int, db: db_dependency) -> StudentInfo:
    """Endpoint to retrieve a specific student's information using their ID."""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentInfo(name=student.name, birthdate=student.birthdate, school_name=student.school_name,
                        major=student.major, graduation_year=student.graduation_year)

@app.delete("/delete_student_info/{student_id}")
async def delete_student_info(student_id: int, db: db_dependency):
    """Endpoint to delete a student's information by their ID."""
    result = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student = result
    db.delete(result)
    db.commit()
    return {"message": f"Student with name {db_student.name} and ID {student_id} deleted successfully."}

@app.delete("/reset_student_info")
async def reset_student_info(db: db_dependency):
    """Endpoint to reset the student information by deleting all records."""
    db.query(models.Student).delete()
    db.commit()
    # Reset the sequence for the ID column
    db.execute(text("ALTER SEQUENCE students_id_seq RESTART WITH 1;"))
    db.commit()
    return {"message": "All student records have been deleted and IDs reset."}
####################################################################################
class StudentCourseInfo(BaseModel):
    """Pydantic model for student course information."""
    # student_id: int // not user friendly because the user doesn't know the course ID
    # course_id: int
    # grade: float

    student_id_number: str 
    course_name: str  
    course_number: str
    teacher: str
    credits: int
    grade:float

@app.post("/add_student_course")
async def add_student_course(student_course: StudentCourseInfo, db: db_dependency):
    """Endpoint to add a student's course information."""
    #checks if the student exists in the database by lookig up student_id_number
    student = db.query(models.Student).filter(models.Student.student_id_number == student_course.student_id_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    #checks if the course exists in the database by looking up course_name, course_number, and teacher
    course = db.query(models.Course).filter(models.Course.course_name == student_course.course_name,
                                             models.Course.course_number == student_course.course_number,
                                             models.Course.teacher == student_course.teacher).first()
    if not course:
        course = models.Course(course_name=student_course.course_name,
                               course_number=student_course.course_number,
                               teacher=student_course.teacher,
                               credits=student_course.credits) #if course does not exist, create a new one
        db.add(course)
        db.commit()
        db.refresh(course)

    # Create a new StudentCourse entry
    db_student_course = models.StudentCourse(student_id=student.id, course_id=course.id, grade=student_course.grade)
    db.add(db_student_course)
    db.commit()
    db.refresh(db_student_course)
    return {"message": f"Student {student.name} added to course {course.course_name} successfully."}


    
    

@app.get("/student_courses")
async def get_student_courses(db: db_dependency) -> List[StudentCourseInfo]:
    """Endpoint to retrieve all student course information from database."""
    student_courses = db.query(models.StudentCourse).all()
    if not student_courses:
        raise HTTPException(status_code=404, detail="No student courses found")
    return [StudentCourseInfo(student_id=sc.student_id, course_id=sc.course_id, grade=sc.grade) for sc in student_courses]

########################################################################################



# class StudentGrade(BaseModel):
#     """Pydantic model for student grade information."""
#     grade: float

# @app.put("/update_student_grade/{student_id}")
# async def update_student_grade(student_id: int, student: StudentInfo, db: db_dependency):
#     """Endpoint to update a student's information."""
#     """Update a student's grade by their ID."""
#     if student.grade < 0:
#         raise HTTPException(status_code=400, detail="Grades cannot be negative")
#     result = db.query(models.Student).filter(models.Student.id == student_id).first() 
#     if not result:
#         raise HTTPException(status_code=404, detail="Student not found")
#     db_student = result
#     db_student.grade = student.grade
#     db.commit()
#     db.refresh(db_student)
#     return {"message": f"Student {db_student.name} had grade updated successfully."}

# @app.delete("/delete_student/{student_id}")
# async def delete_student(student_id: int, db: db_dependency):
#     """Endpoint to delete a student's information."""
#     """Delete a student by their ID."""
#     result = db.query(models.Student).filter(models.Student.id == student_id).first()
#     if not result:
#         raise HTTPException(status_code=404, detail="Student not found")
#     db_student = result
#     db.delete(result)
#     db.commit()
#     return {"message": f"Student with name {db_student.name} and ID {student_id} deleted successfully."}

# @app.get("/students")
# async def get_students(db: db_dependency) -> List[StudentInfo]:
#     """Endpoint to retrieve all students."""
#     """Get all students from the database."""
#     students = db.query(models.Student).all()
#     if not students:
#         raise HTTPException(status_code=404, detail="No students found")
#     return [StudentInfo(name=student.name, grade=student.grade) for student in students]

# @app.get("/student/{student_id}")
# async def get_student(student_id: int, db: db_dependency) -> StudentInfo:
#     """Endpoint to retrieve a specific student's information using their ID."""
#     student = db.query(models.Student).filter(models.Student.id == student_id).first()
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
#     return StudentInfo(name=student.name, grade=student.grade)

# @app.get("/stats")
# async def get_stats(db: db_dependency):
#     """Endpoint to calculate and return statistics of student grades."""
#     """Calculate statistics from the database."""
#     students = db.query(models.Student).all()
#     if not students:
#         raise HTTPException(status_code=404, detail="No students found")
    
#     grades = [student.grade for student in students]
#     min_grade = round(min(grades),2)
#     max_grade = round(max(grades),2)
#     avg_grade = round(sum(grades) / len(grades),2)

#     return {
#         "min_grade": min_grade,
#         "max_grade": max_grade,
#         "average_grade": avg_grade
#     }

# @app.get("/student_letter_grades")
# async def get_student_letter_grades(db: db_dependency):
#     """Endpoint to retrieve letter grades for all students."""
#     students = db.query(models.Student).all()
#     if not students:
#         raise HTTPException(status_code=404, detail="No students found")
    
#     letter_grades = {}
#     for student in students:
#         letter_grades[student.name] = get_letter_grade(student.grade) #adds key value pair to the dictionary
    
#     return letter_grades

# @app.get("/student_letter_grade/{student_id}")
# async def get_student_letter_grade(student_id: int, db: db_dependency):
#     """Endpoint to retrieve a specific student's letter grade using their ID."""
#     student = db.query(models.Student).filter(models.Student.id == student_id).first()
#     if not student:
#         raise HTTPException(status_code=404, detail="Student not found")
    
#     letter_grade = get_letter_grade(student.grade)
#     return {"name": student.name, "letter_grade": letter_grade}

# @app.delete("/reset_db")
# async def reset_db(db: db_dependency):
#     """Endpoint to reset the database by deleting all student records."""
#     db.query(models.Student).delete()
#     db.commit()
#     #reset the sequence for the ID column
#     db.execute(text("ALTER SEQUENCE students_and_grades_id_seq RESTART WITH 1;"))
#     db.commit()
#     return {"message": "All student records have been deleted and IDs reset."}