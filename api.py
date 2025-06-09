from fastapi import FastAPI, HTTPException, Depends
#from sqlalchemy import create_engine, Column, Integer, String
from  pydantic import BaseModel
from typing import Annotated, List
from student_gradebook_api import add_student_info, calculate_stats_from_file
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
    db_student = models.Student(name=student.name, grade=student.grade)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    #add_student_info(student.name, student.grade)
    return {"message": f"Student {student.name} with grade {student.grade} added successfully."}

