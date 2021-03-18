from __future__ import annotations
from src.Validations.Validation import Validation


class CourseOpenEnrollmentValidation(Validation):
    """
    required kwargs
    student: Student, course_section: CourseSection
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CourseOpenEnrollmentValidation.__instance == None:
            CourseOpenEnrollmentValidation()
        return CourseOpenEnrollmentValidation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if CourseOpenEnrollmentValidation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CourseOpenEnrollmentValidation.__instance = self

    def is_valid(self, report, **kwargs):
        print("course open enrollment validator doing its thang")
        course_section = kwargs['course_section']

        validation = self.__class__.__name__
        success = course_section.enrollment_open

        if course_section.enrollment_open:
            msg = "Course is open for enrollment"
        else:
            msg = "Course is not open for enrollment"

        report.add_data(validation=validation, success=success, msg=msg)
