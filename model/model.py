from typing import List
from pydantic import BaseModel


class Course(BaseModel):
    Name: str
    Room: str
    WeekStart: int
    WeekEnd: int
    SectionStart: int
    SectionEnd: int
    # 1~7
    DayOfWeek: int


class CourseForm(BaseModel):
    Courses: List[Course]
    WeekOrder: int
