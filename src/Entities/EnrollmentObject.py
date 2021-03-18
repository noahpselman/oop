from __future__ import annotations
from src.util import make_course_index


class EnrollmentObject():
    """
    Holds data relevant to enrollments to be used
    in other processes
    Even those it's pretty much just data, it's
    used enough where defining a class makes sense
    """

    def __init__(self, *,
                 student_id, section_number,
                 course_id, department, quarter, type, state):
        """
        all parameters are strings
        """
        self.student_id = student_id
        self.section_number = section_number
        self.course_id = course_id
        self.department = department
        self.course_index = make_course_index(
            course_id=self.course_id, department=self.department)
        self.quarter = quarter
        self.graded_type = type
        self.state = state
        """
        having type attributes is a sign that a pattern could be used
        grading isn't part of my prototype so I'm triaging that re-factor
        i'd probably make grade its own interface with a Regular and P/F
        version
        that way the course_section won't care about the type of enrollment
        """

    def jsonify(self):
        result = self.__dict__
        return result

    def __repr__(self) -> str:
        return f"Enrollment Obj student {self.student_id} in {self.department} {self.course_id}/{self.section_number}, quarter: {self.quarter}"
