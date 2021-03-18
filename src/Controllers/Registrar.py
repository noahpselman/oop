from __future__ import annotations
from src.Validations.ValidationReport import DropValidationReport, RegisterValidationReport, ValidationReport
from src.Validations.CourseHasNotFinishedValidation import CourseHasNotFinishedValidation
from src.Validations.AlreadyInCourseValidation import AlreadyInCourseValidation
from src.Validations.CourseHasEmptySeatValidation import CourseHasEmptySeatValidation
from src.Validations.OverloadPermissionValidation import OverloadPermissionValidation
from src.Validations.InstructorPermissionValidation import InstructorPermissionValidation
from src.Validations.NotInCourseValidation import NotInCourseValidation
from src.Validations.TimeSlotValidation import TimeSlotValidation
from src.Validations.StudentRestrictionValidation import StudentRestrictionValidation
from src.Validations.LabValidation import LabValidation
from src.Validations.PrereqValidation import PrereqValidation
from src.Entities.EnrollmentObject import EnrollmentObject
from src.Database.EnrollmentObjectMapper import EnrollmentObjectMapper
from src.Validations.Validator import Validator


class Registrar():
    """
    singleton
    controller responsible for handling changes of enrollments:
        registering student for a course
        dropping a course

    has class attributes corresponding to the checks required
    for a student to register in a course section or to drop
    one
    """
    __instance = None

    REGISTER_VALIDATIONS = ([
        PrereqValidation,
        LabValidation,
        StudentRestrictionValidation,
        TimeSlotValidation,
        NotInCourseValidation,
        InstructorPermissionValidation,
        OverloadPermissionValidation,
        CourseHasEmptySeatValidation
    ])

    DROP_VALIDATIONS = ([
        AlreadyInCourseValidation,
        CourseHasNotFinishedValidation
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

    def __create_validator(self, student, course_section):
        validator = Validator(student, course_section)
        return validator

    def register_for_lab(self, *,
                         student: Student, course_section: CourseSection,
                         lab_section: CourseSection):

        validator = self.__create_validator(student, lab_section)
        lab_report = RegisterValidationReport()
        validator.check_for_failures(
            self.REGISTER_VALIDATIONS, lab_report)
        print("lab report", lab_report.jsonify())

        if not lab_report.is_successful:
            return lab_report

        else:
            validator = self.__create_validator(student, course_section)
            section_report = RegisterValidationReport()
            validations = [
                val for val in self.REGISTER_VALIDATIONS if val is not LabValidation]
            validator.check_for_failures(validations, section_report)
            print("section report", section_report.jsonify())

            if not section_report.is_successful:
                return section_report

            else:
                section_result = self.__add_to_db(
                    student=student, course_section=course_section)
                section_report.db_updated = True

                if section_result:
                    lab_result = self.__add_to_db(
                        student=student, course_section=lab_section)
                    lab_report.db_updated = True

                    return lab_report

    def register_for_course(self, *, student: Student,
                            course_section: CourseSection) -> ValidationReport:
        """
        validates students eligibility to enroll
        instructs enrollment object mapper to make a
        database transaction
        returns a validation report action that gives
        details on the process

        """
        validator = self.__create_validator(student, course_section)
        validation_report = RegisterValidationReport()
        validator.check_for_failures(
            self.REGISTER_VALIDATIONS, validation_report)

        print(validation_report.jsonify())

        if validation_report.is_successful:

            # TODO delegate this to enrollment factory
            result = self.__add_to_db(
                student=student, course_section=course_section)
            validation_report.db_updated = result
            return validation_report

        else:
            validation_report.db_updated = False
            return validation_report

    def __add_to_db(self, *, student: Student, course_section: CourseSection):
        enrollment = EnrollmentObject(
            student_id=student.id,
            section_number=course_section.section_number,
            course_id=course_section.course_id,
            department=course_section.department,
            quarter=course_section.quarter,
            type='REGULAR',
            state='COMPLETE'
        )
        mapper = EnrollmentObjectMapper.getInstance()
        result = mapper.insert(enrollable=enrollment)
        return result

    def drop_course(self, student: Student, course_section: CourseSection) -> ValidationReport:
        """
        validates students eligibility to drop a course
        instructs enrollment object mapper to make a
        database transaction
        returns a validation report action that gives
        details on the process

        """
        validator = self.__create_validator(student, course_section)
        validation_report = DropValidationReport()
        validator.check_for_failures(
            self.DROP_VALIDATIONS, validation_report)

        if validation_report.is_successful:

            drop_enrollment_kwargs = {
                'section_number': course_section.section_number,
                'course_id': course_section.course_id,
                'department': course_section.department,
                'quarter': course_section.quarter,
                'student_id': student.id
            }
            mapper = EnrollmentObjectMapper.getInstance()
            success = mapper.delete(**drop_enrollment_kwargs)
            validation_report.db_updated = success

            return validation_report
        else:
            validation_report.db_updated = False
            return validation_report
