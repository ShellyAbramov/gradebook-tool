from fastapi import FastAPI, HTTPException, Depends
from  pydantic import BaseModel
from typing import Annotated, List, Optional
#from student_gradebook_api import add_student_info, calculate_stats_from_file
from student_gradebook import get_letter_grade  # Importing the function to get letter grades
#student_info, student_letter_grades, student_gradebook_stats, calculate_stats_from_file
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date
from sqlalchemy.exc import IntegrityError
from fastapi.middleware.cors import CORSMiddleware
from gpa import student_gpa_in_records  # Importing the GPA calculation functions


app = FastAPI()

# CORS middleware to allow requests from any origin
origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from the specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)


models.Base.metadata.create_all(bind=engine)  # Create tables in the database


def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Student Gradebook API"} #for testing purposes


class StudentInfo(BaseModel):
    """Pydantic model for student information."""
    name: str
    birthdate: date 
    major: str
    graduation_year: int
    gpa: Optional[float] = None  # GPA is optional, will be calculated later when adding courses
    student_id_number: str  

@app.post("/add_student_info") #API makes a connection to the database here as well
async def add_student(student: StudentInfo, db: db_dependency):
    """Endpoint to add a student's information."""
    
    db_student = models.Student(name=student.name, birthdate=student.birthdate,
                                major=student.major, graduation_year=student.graduation_year, 
                                student_id_number=student.student_id_number)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return {"message": f"Student {student.name} added successfully."}

class UpdateStudentInfo(BaseModel):
    """Pydantic model for updating student information."""
    name: Optional [str]
    birthdate: Optional[date]
    major: Optional[str]
    graduation_year: Optional[int]
    student_id_number: Optional[str] 

@app.put("/update_student_info/{student_id}")
async def update_student_info(student_id: int, student: UpdateStudentInfo, db: db_dependency):
    """Endpoint to update a student's information."""
    """Update a student's information by their ID."""
    result = db.query(models.Student).filter(models.Student.id == student_id).first() 
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db_student = result
    if student.name is not None:
        db_student.name = student.name
    if student.birthdate is not None:
        db_student.birthdate = student.birthdate
    if student.major is not None:
        db_student.major = student.major
    if student.graduation_year is not None:
        db_student.graduation_year = student.graduation_year
    if student.student_id_number is not None:
        db_student.student_id_number = student.student_id_number
    
    db.commit()
    db.refresh(db_student)
    return {"message": f"Student {db_student.name}'s information updated successfully."} 



@app.get("/student_info")
async def get_student_info(db: db_dependency) -> List[StudentInfo]:
    """Endpoint to retrieve all students' information."""
    """Get all students from the database."""
    students = db.query(models.Student).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return [StudentInfo(name=student.name, birthdate=student.birthdate, major=student.major, 
                        graduation_year=student.graduation_year,
                        gpa=student.GPA,student_id_number=student.student_id_number) for student in students]

@app.get("/student_info/{student_id}")
async def get_student_info_by_id(student_id: int, db: db_dependency) -> StudentInfo:
    """Endpoint to retrieve a specific student's information using their ID."""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentInfo(name=student.name, birthdate=student.birthdate, 
                        major=student.major, graduation_year=student.graduation_year,
                        gpa=student.GPA, student_id_number=student.student_id_number)

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
    # Delete student-course associations FIRST
    db.query(models.StudentCourse).delete()
    # THEN delete students
    db.query(models.Student).delete()
    db.commit()
        
    # Reset the sequences
    db.execute(text("ALTER SEQUENCE students_id_seq RESTART WITH 1;"))
    db.execute(text("ALTER SEQUENCE student_courses_id_seq RESTART WITH 1;"))
    db.commit()
    return {"message": "All student records and course enrollments have been deleted and IDs reset."}

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
                               credits=student_course.credits,
                               number_of_students=0) #if course does not exist, create a new one
        db.add(course)
        db.commit()
        db.refresh(course)

    # Create a new StudentCourse entry
    try:
        db_student_course = models.StudentCourse(student_id=student.id, course_id=course.id, grade=student_course.grade)
        db.add(db_student_course)

        #increment the number of students in the course
        course.number_of_students = (course.number_of_students or 0) + 1
        db.commit()
        db.refresh(db_student_course)

        #call the function to calculate and update the student's GPA
        student_gpa_in_records(student.student_id_number, db)

        return {"message": f"Student {student.name} added to course {course.course_name} and GPA updated successfully."}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="This student is already enrolled in this course.")


@app.get("/student_courses")
async def get_student_courses(db: db_dependency) -> List[StudentCourseInfo]:
    """Endpoint to retrieve all student course information from database."""
    student_courses = db.query(models.StudentCourse).all()
    if not student_courses:
        raise HTTPException(status_code=404, detail="No student courses found")
    return [StudentCourseInfo(student_id=sc.student_id, course_id=sc.course_id, grade=sc.grade) for sc in student_courses]


@app.delete("/reset_courses")
async def reset_courses(db: db_dependency):
    """Endpoint to reset the student courses by deleting all records."""
    db.query(models.Course).delete()
    db.commit()
    # Reset the sequence for the ID column
    db.execute(text("ALTER SEQUENCE courses_id_seq RESTART WITH 1;"))
    db.commit()
    return {"message": "All course records have been deleted and IDs reset."}
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