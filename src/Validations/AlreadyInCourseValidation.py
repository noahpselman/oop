from __future__ import annotations
from src.Validations.Validation import Validation


class AlreadyInCourseValidation(Validation):
    """
    required kwargs
    student: Student, course_section: CourseSection
    checks if student is already in the course
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if AlreadyInCourseValidation.__instance == None:
            AlreadyInCourseValidation()
        return AlreadyInCourseValidation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if AlreadyInCourseValidation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            AlreadyInCourseValidation.__instance = self

    def is_valid(self, report, **kwargs):
        print("already enrolled validator doing its thang")
        student = kwargs['student']
        course_section = kwargs['course_section']

        current_courses = student.get_courses_by_quarter(
            course_section.quarter)
        already_enrolled = False
        for course in current_courses:

            if course.course_section_name == course_section.course_section_name:
                already_enrolled = True
                break

        validation = self.__class__.__name__
        success = already_enrolled
        if already_enrolled:
            msg = "You are already enrolled in this course"
        else:
            msg = "You're not already enrolled in this course"

        report.add_data(validation=validation, success=success, msg=msg)
