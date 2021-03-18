from __future__ import annotations
from src.Validations.Validation import Validation


class CourseHasNotFinishedValidation(Validation):
    """
    required kwargs
    student: Student, course_section: CourseSection
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CourseHasNotFinishedValidation.__instance == None:
            CourseHasNotFinishedValidation()
        return CourseHasNotFinishedValidation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if CourseHasNotFinishedValidation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CourseHasNotFinishedValidation.__instance = self

    def is_valid(self, report, **kwargs):
        print("course has not started validator doing its thang")
        course_section = kwargs['course_section']

        success = course_section.state in ('PRESTART', 'ONGOING')
        validation = self.__class__.__name__

        if success:
            msg = "Course is has not started and can be dropped"
        else:
            msg = "Course is has started and cannot be dropped"

        report.add_data(validation=validation, success=success, msg=msg)
