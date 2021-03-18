from __future__ import annotations
from src.Validations.Validation import Validation


class InstructorPermissionValidation(Validation):
    """
    required kwargs
    student: Student, course_section: CourseSection
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if InstructorPermissionValidation.__instance == None:
            InstructorPermissionValidation()
        return InstructorPermissionValidation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if InstructorPermissionValidation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            InstructorPermissionValidation.__instance = self

    def is_valid(self, report: ValidationReport, **kwargs):
        print("instructor permission validator doing its thang")
        course_section = kwargs['course_section']

        validation = self.__class__.__name__

        if not course_section.instructor_permission_required:
            success = True
            msg = "Instructor permission is not required for this class"
        else:
            success = False
            msg = "Instructor permission is required for this class"

        report.add_data(validation=validation, success=success, msg=msg)
