from __future__ import annotations
from src.util import get_current_quarter

from src.Database.DatabaseHelper import DatabaseHelper
from src.Entities.CourseSection import CourseSection
from src.Database.EnrollmentObjectMapper import EnrollmentObjectMapper
from src.Entities.EnrollmentObject import EnrollmentObject


class EnrollmentFactory():

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if EnrollmentFactory.__instance == None:
            EnrollmentFactory()
        return EnrollmentFactory.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if EnrollmentFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            EnrollmentFactory.__instance = self

    def build_enrollment(self, data):
        enrollment_object = EnrollmentObject(**data)
        print("enrollment object from enrollment factory",
              enrollment_object.jsonify())
        return enrollment_object

    def build_enrollments(self, data):
        return [self.build_enrollment(row) for row in data]

    def build_enrollments_from_id(self, id: str):
        mapper = EnrollmentObjectMapper.getInstance()
        loaded_data = mapper.load(id)
        print("loaded data from enrollment factory", loaded_data)
        return self.build_enrollments(loaded_data)

    def create_new_enrollment(self, student: Student, course_section: CourseSection):
        enrollment_data = {
            'section_number': course_section.section_number,
            'course_id': course_section.course_id,
            'department': course_section.department,
            'quarter': get_current_quarter(),
            'student_id': student.id,
            'type': 'REGULAR',
            'state': 'COMPLETE'
        }
        db_helper = DatabaseHelper.getInstance()
        return db_helper.insert_new_enrollment(enrollment_data)
