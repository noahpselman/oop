from __future__ import annotations
from src.Entities.CourseSection import CourseSection
from src.Database.DatabaseHelper import DatabaseHelper
from src.util import make_section_index, get_system_email


class Request():

    def __init__(self, *, student: Student, course_section: CourseSection):
        self.student = student
        self.course_section = course_section
        self._state = ""

    @property
    def student_id(self):
        return self.student.id

    @property
    def section_number(self):
        return self.course_section.section_number

    @property
    def course_id(self):
        return self.course_section.course_id

    @property
    def department(self):
        return self.course_section.department

    @property
    def quarter(self):
        return self.course_section.quarter

    @property
    def state(self):
        return self._db_status

    @property
    def recipient_email(self):
        pass

    @property
    def msg(self):
        pass


class InstructorPermissionRequest(Request):
    def __init__(self, *, student: Student, course_section: CourseSection):
        super().__init__(student=student, course_section=course_section)
        self._db_status = "TENTATIVE"

    @property
    def msg(self):
        msg = f"This is an automated notification.  Student {self.student_id}" +\
            f"requests a spot in the following course: {self.course_section.course_section_name}" +\
            "Please log into your account to approve/reject"
        return msg

    @property
    def recipient_email(self):
        """

        """
        return self.course_section.instructor_email


class OverloadPermissionRequest(Request):
    def __init__(self, *, student: Student, course_section: CourseSection):
        super().__init__(student=student, course_section=course_section)
        self._db_status = "PENDING"

    @property
    def msg(self):
        msg = f"This is an automated notification.  Student {self.student_id}" +\
            f"requires an overload to enroll in the following course: {self.course_section.course_section_name}" +\
            "Please log into your account to approve/reject"
        return msg

    @property
    def recipient_email(self):
        db_helper = DatabaseHelper.getInstance()
        return db_helper.load_department_email(department=self.course_section.department)
