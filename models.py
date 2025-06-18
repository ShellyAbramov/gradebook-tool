from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, UniqueConstraint
from database import Base
from sqlalchemy.orm import relationship

class Student(Base):
    """SQLAlchemy model for the Student table."""
    #Table for student information
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    birthdate = Column(String)  # Assuming birthdate is stored as string in 'YYYY-MM-DD' format
    school_name = Column(String)  
    major = Column(String) 
    graduation_year = Column(Integer)
    GPA = Column(Float)


    course_association = relationship("StudentCourse", back_populates="student", cascade="all, delete")
    #helps connect the student to the course they are enrolled in


#Table for course information
class Course(Base):
    """SQLAlchemy model for the Course table."""
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    credits = Column(Integer)
    teacher = Column(String) 

    student_association = relationship("StudentCourse", back_populates="course") #a course can have many students enrolled in it

#Student course association table
class StudentCourse(Base):
    """SQLAlchemy model for the StudentCourse association table."""
    __tablename__ = 'student_courses'

    id = Column(Integer, primary_key=True, index=True) 

    #foreign keys to link students and courses tables
    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)

    grade = Column(Float)  # Grade for the course

    student = relationship("Student", back_populates="course_association")
    course = relationship("Course", back_populates="student_association")

    __table_args__ = (UniqueConstraint('student_id', 'course_id', name='_student_course_uc'),)  # Ensure unique student-course pairs
