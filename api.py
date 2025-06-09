from fastapi import FastAPI
from  pydantic import BaseModel
from student_gradebook import add_student_info, calculate_stats_from_file
#student_info, student_letter_grades, student_gradebook_stats, calculate_stats_from_file

app = FastAPI()
# class Student(BaseModel):
#     name: str
#     grade: float

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Student Gradebook API"} #for testing purposes


class StudentInfo(BaseModel):
    """Pydantic model for student information."""
    name: str
    grade: float

@app.post("/add_student")
async def add_student(student: StudentInfo):
    """Endpoint to add a student's information."""
    add_student_info(student.name, student.grade)
    return {"message": f"Student {student.name} with grade {student.grade} added successfully."}


@app.get("/stats")
async def get_stats():
    """Endpoint to get the statistics of the student gradebook."""
    stats = calculate_stats_from_file()
    return {
        "min_grade": stats['min_grade'],
        "max_grade": stats['max_grade'],
        "average_grade": stats['avg_grade']
    }

