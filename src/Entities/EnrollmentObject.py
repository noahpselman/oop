from __future__ import annotations


class EnrollmentObject():

    def __init__(self, **kwargs):
        self.student_id = kwargs['student_id']
        self.section_number = kwargs['section_number']
        self.course_id = kwargs['course_id']
        self.department = kwargs['department']
        self.quarter = kwargs['quarter']
        self.graded_type = kwargs['type']

        # having type attributes is a sign that a pattern could be used
        # grading isn't part of my prototype so I'm triaging that re-factor
        # i'd probably make grade its own interface with a Regular and P/F
        # version
        # that way the course_section won't care about the type of enrollment

    def jsonify(self):
        result = self.__dict__
        return result

    def __repr__(self) -> str:
        return f"student {self.student_id} in {self.department} {self.course_id}/{self.section_number}, quarter: {self.quarter}"
