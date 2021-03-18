from __future__ import annotations
from src.Validations.Validation import Validation


class CourseHasEmptySeatValidation(Validation):
    """
    required kwargs
    student: Student, course_section: CourseSection
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CourseHasEmptySeatValidation.__instance == None:
            CourseHasEmptySeatValidation()
        return CourseHasEmptySeatValidation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if CourseHasEmptySeatValidation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CourseHasEmptySeatValidation.__instance = self

    def is_valid(self, report, **kwargs):
        print("course open enrollment validator doing its thang")
        course_section = kwargs['course_section']

        validation = self.__class__.__name__

        if course_section.get_enrollment_total() < course_section.capacity:
            success = True
            msg = "Course has an open seat"
        else:
            success = False
            msg = "Course is full"

        report.add_data(validation=validation, success=success, msg=msg)
