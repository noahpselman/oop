from __future__ import annotations
from src.Validations.Validation import Validation


class OverloadPermissionValidation(Validation):
    """
    required kwargs
    student: Student, course_section: CourseSection
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if OverloadPermissionValidation.__instance == None:
            OverloadPermissionValidation()
        return OverloadPermissionValidation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if OverloadPermissionValidation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            OverloadPermissionValidation.__instance = self

    def is_valid(self, report, **kwargs):
        print("overload permission validator doing its thang")
        student = kwargs['student']

        validation = self.__class__.__name__

        if student.max_enrollment <= len(student.current_courses):
            success = False
            msg = "You are at your maximum enrollment.  An overload request " +\
                "from your department head is required."
        else:
            success = True
            msg = "You will not exceed your maximum number of enrolled courses"
        report.add_data(validation=validation, success=success, msg=msg)
