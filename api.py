from fastapi import FastAPI, HTTPException, Depends
#from sqlalchemy import create_engine, Column, Integer, String
from  pydantic import BaseModel
from typing import Annotated, List
from student_gradebook_api import add_student_info, calculate_stats_from_file
from student_gradebook import get_letter_grade  # Importing the function to get letter grades
#student_info, student_letter_grades, student_gradebook_stats, calculate_stats_from_file
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


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
models.Base.metadata.create_all(bind=engine)  # Create tables in the database


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Student Gradebook API"} #for testing purposes


class StudentInfo(BaseModel):
    """Pydantic model for student information."""
    name: str
    grade: float

@app.post("/add_student") #API makes a connection to the database here as well
async def add_student(student: StudentInfo, db: db_dependency):
    """Endpoint to add a student's information."""
    if student.grade < 0:
        raise HTTPException(status_code=400, detail="Grades cannot be negative")
    db_student = models.Student(name=student.name, grade=round(student.grade,2))
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    #add_student_info(student.name, student.grade)
    return {"message": f"Student {student.name} with grade {student.grade} added successfully."}

@app.put("/update_student_grade/{student_id}")
async def update_student_grade(student_id: int, student: StudentInfo, db: db_dependency):
    """Endpoint to update a student's information."""
    """Update a student's grade by their ID."""
    if student.grade < 0:
        raise HTTPException(status_code=400, detail="Grades cannot be negative")
    result = db.query(models.Student).filter(models.Student.id == student_id).first() 
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student = result
    db_student.grade = student.grade
    db.commit()
    db.refresh(db_student)
    return {"message": f"Student {db_student.name} had grade updated successfully."}

@app.delete("/delete_student/{student_id}")
async def delete_student(student_id: int, db: db_dependency):
    """Endpoint to delete a student's information."""
    """Delete a student by their ID."""
    result = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student = result
    db.delete(result)
    db.commit()
    return {"message": f"Student with name {db_student.name} and ID {student_id} deleted successfully."}

@app.get("/students")
async def get_students(db: db_dependency) -> List[StudentInfo]:
    """Endpoint to retrieve all students."""
    """Get all students from the database."""
    students = db.query(models.Student).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return [StudentInfo(name=student.name, grade=student.grade) for student in students]

@app.get("/student/{student_id}")
async def get_student(student_id: int, db: db_dependency) -> StudentInfo:
    """Endpoint to retrieve a specific student's information using their ID."""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return StudentInfo(name=student.name, grade=student.grade)

@app.get("/stats")
async def get_stats(db: db_dependency):
    """Endpoint to calculate and return statistics of student grades."""
    """Calculate statistics from the database."""
    students = db.query(models.Student).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    
    grades = [student.grade for student in students]
    min_grade = round(min(grades),2)
    max_grade = round(max(grades),2)
    avg_grade = round(sum(grades) / len(grades),2)

    return {
        "min_grade": min_grade,
        "max_grade": max_grade,
        "average_grade": avg_grade
    }

@app.get("/student_letter_grades")
async def get_student_letter_grades(db: db_dependency):
    """Endpoint to retrieve letter grades for all students."""
    students = db.query(models.Student).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    
    letter_grades = {}
    for student in students:
        letter_grades[student.name] = get_letter_grade(student.grade) #adds key value pair to the dictionary
    
    return letter_grades

@app.get("/student_letter_grade/{student_id}")
async def get_student_letter_grade(student_id: int, db: db_dependency):
    """Endpoint to retrieve a specific student's letter grade using their ID."""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    letter_grade = get_letter_grade(student.grade)
    return {"name": student.name, "letter_grade": letter_grade}