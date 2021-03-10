from __future__ import annotations
from src.Validations.Validation import AlreadyInCourseValidation, CourseHasEmptySeatValidator, CourseHasNotStartedValidator, CourseOpenEnrollmentValidator, InstructorPermissionValidator, NotInCourseValidation, OverloadPermissionValidation, PrereqValidation, StudentRestrictionValidation, TimeSlotValidation
from src.Database.DatabaseHelper import DatabaseHelper
from src.Entities.Validator import Validator


class Registrar():
    __instance = None

    REGISTER_VALIDATIONS = ([
        PrereqValidation,
        StudentRestrictionValidation,
        TimeSlotValidation,
        NotInCourseValidation,
        InstructorPermissionValidator,
        OverloadPermissionValidation,
        CourseHasEmptySeatValidator
    ])

    DROP_VALIDATIONS = ([
        AlreadyInCourseValidation,
        CourseHasNotStartedValidator
    ])

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Registrar.__instance == None:
            Registrar()
        return Registrar.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Registrar.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Registrar.__instance = self

    def register_for_course(self, student: Student, course_section: CourseSection):
        print("register for course called in student")
        validator = Validator(student, course_section)
        validation_report = validator.check_for_failures(
            self.REGISTER_VALIDATIONS)
        print("validation report", validation_report)
        if validation_report['success']:
            new_enrollment_kwargs = {
                'section_number': course_section.section_number,
                'course_id': course_section.course_id,
                'department': course_section.department,
                'quarter': course_section.quarter,
                'student_id': student.id,
                'type': 'REGULAR',
                'state': 'COMPLETE'
            }

            db_helper = DatabaseHelper.getInstance()
            result = db_helper.insert_new_enrollment(new_enrollment_kwargs)
            validation_report['db_updated'] = result
            return validation_report

        else:
            return validation_report

    def drop_course(self, student: Student, course_section: CourseSection):
        print("drop course called by registrar")
        validator = Validator(student, course_section)
        validation_report = validator.check_for_failures(self.DROP_VALIDATIONS)
        if validation_report['success']:

            drop_enrollment_kwargs = {
                'section_number': course_section.section_number,
                'course_id': course_section.course_id,
                'department': course_section.department,
                'quarter': course_section.quarter,
                'student_id': student.id
            }
            db_helper = DatabaseHelper.getInstance()
            success = db_helper.delete_enrollment(**drop_enrollment_kwargs)
            validation_report['db_updated'] = success

            return validation_report
        else:
            validation_report['db_updated'] = False
            return validation_report
