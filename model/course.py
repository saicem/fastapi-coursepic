class Course:
    name: str
    room: str
    week_start: str
    week_end: str
    section_start: str
    section_end: str
    day_of_week: str
    teacher: str
    credit: str

    def __init__(self, course_json) -> None:
        self.name = course_json["name"]
        self.room = course_json["room"]
        self.week_start = course_json["weekStart"]
        self.week_end = course_json["weekEnd"]
        self.section_start = course_json["sectionStart"]
        self.section_end = course_json["sectionEnd"]
        self.day_of_week = course_json["dayOfWeek"]
        self.teacher = course_json["teacher"]
        self.credit = course_json["credit"]


def ReadCourses(courses_json: str):
    course_list = []
    for course in courses_json:
        course_list.append(Course(course))
    return course_list
