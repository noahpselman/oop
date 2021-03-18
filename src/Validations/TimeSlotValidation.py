from __future__ import annotations
from src.Validations.Validation import Validation


class TimeSlotValidation(Validation):
    """
    required kwargs
    student: Student, course_section: CourseSection
    """
    __instance = None

    @ staticmethod
    def getInstance():
        """ Static access method. """
        if TimeSlotValidation.__instance == None:
            TimeSlotValidation()
        return TimeSlotValidation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if TimeSlotValidation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            TimeSlotValidation.__instance = self

    def is_valid(self, report, **kwargs):
        print("time slot validator doing its thang")
        student = kwargs['student']
        course_section = kwargs['course_section']

        current_courses = student.get_courses_by_quarter(
            course_section.quarter)
        overlaps = ([c.course_section_name for c in current_courses
                     if not c.timeslot.no_overlap(course_section.timeslot)])

        validation = self.__class__.__name__
        success = not overlaps
        msg = self.__write_msg(overlaps)

        report.add_data(validation=validation, success=success, msg=msg)

    def __write_msg(self, overlaps):
        print("overlaps", type(overlaps))
        if not overlaps:
            return "You have no time conflicts"
        else:
            return "The following coures are causing time conflicts: " + \
                ', '.join(overlaps)
