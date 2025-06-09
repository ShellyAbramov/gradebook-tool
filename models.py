from sqlalchemy import Column, Integer, String, Float
from database import Base

class Student(Base):
    """SQLAlchemy model for the Student table."""
    __tablename__ = 'students_and_grades'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique = True, index=True)
    grade = Column(Float)

