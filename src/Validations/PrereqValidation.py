from __future__ import annotations
from src.Validations.Validation import Validation


class PrereqValidation(Validation):

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if PrereqValidation.__instance == None:
            PrereqValidation()
        return PrereqValidation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if PrereqValidation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            PrereqValidation.__instance = self

    def is_valid(self, report: ValidationReport, **kwargs):
        """
        required kwargs
        student: Student, course_section: CourseSection
        """
        print("prereq validator doing it's thang")
        student = kwargs['student']
        course_section = kwargs['course_section']
        prereqs = course_section.prereqs
        course_history = [
            c.course_index for c in student.course_history]
        unmet_prereqs = [
            prereq for prereq in prereqs if prereq not in course_history]
        validation = self.__class__.__name__
        success = not unmet_prereqs
        msg = self.__write_msg(unmet_prereqs)
        report.add_data(validation=validation, success=success, msg=msg)

    def __write_msg(self, unmet_prereqs):
        print("unmet_prereqs", unmet_prereqs)
        if not unmet_prereqs:
            return "You have met all the prereqs"
        else:
            return "You have not completed the following prereqs: " + \
                ', '.join(unmet_prereqs)
