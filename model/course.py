class Course:
    name: str
    room: str
    week_start: str
    week_end: str
    week_span: str
    section_start: str
    section_end: str
    class_span: str
    day_of_week: str
    teacher: str
    credit: str
    status: str

    def __init__(self, course_json) -> None:
        self.name = course_json["name"]
        self.room = course_json["room"]
        self.week_start = course_json["weekStart"]
        self.week_end = course_json["weekEnd"]
        self.week_span = course_json["weekSpan"]
        self.section_start = course_json["sectionStart"]
        self.section_end = course_json["sectionEnd"]
        self.class_span = course_json["sectionSpan"]
        self.day_of_week = course_json["dayOfWeek"]
        self.teacher = course_json["teacher"]
        self.credit = course_json["credit"]
        self.status = course_json["status"]


def ReadCourses(courses_json: str):
    course_list = []
    for course in courses_json:
        course_list.append(Course(course))
    return course_list
