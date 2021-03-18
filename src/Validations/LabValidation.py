from __future__ import annotations
from src.Validations.Validation import Validation


class LabValidation(Validation):

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if LabValidation.__instance == None:
            LabValidation()
        return LabValidation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if LabValidation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            LabValidation.__instance = self

    def is_valid(self, report, **kwargs):
        """
        required kwargs
        student: Student, course_section: CourseSection
        """
        course_section = kwargs['course_section']
        lab = course_section.lab
        validation = self.__class__.__name__

        if lab:
            student = kwargs['student']
            current_courses = student.get_courses_by_quarter(
                course_section.quarter)
            current_course_indexes = [c.course_info for c in current_courses]
            in_lab = lab.course_info in current_course_indexes
            success = in_lab
            msg = self.__write_msg(in_lab, lab)
        else:
            success = True
            msg = "No lab required"

        report.add_data(validation=validation, success=success, msg=msg)

    def __write_msg(self, in_lab, lab):
        print("in_lab", in_lab)
        if in_lab:
            return "You are enrolled in the lab"
        else:
            return f"You are not enrolled in the lab: {lab}"
