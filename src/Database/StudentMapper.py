from __future__ import annotations
from src.Factories.CourseSectionFactory import CourseSectionFactory
from src.Factories.EnrollmentFactory import EnrollmentFactory
from src.Database.DatabaseHelper import DatabaseHelper
from typing import List
# from src.classes.Exceptions import StudentHasNoIDExeception
from src.Database.Mapper import Mapper
from src.Constants.Restrictions import *
from src.Entities.User import User


"""
Kind of like a factory but only from db
Also can load in chunks - not sure if this
will be useful
"""


# this will eventually find somewhere else to live
RESTRICTION_MAPPER = {
    "LIBRARY": LibraryRestriction,
    "ACADEMIC ADVISOR": AcademicAdvisorRestriction,
    "TUITION": TuitionRestriction,
    "SUSPENSION": SuspensionRestriction,
    "IMMUNIZATION": ImmunizationRestriction
}


class StudentMapper(Mapper):

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if StudentMapper.__instance == None:
            StudentMapper()
        return StudentMapper.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if StudentMapper.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            StudentMapper.__instance = self
            super().__init__()

    def load(self, user: User):
        # print(self.db_helper)

        print(f"student mapper load: userid is {user.id}")
        student_data = self.db_helper.load_student_by_id(user.id)

        if student_data['fulltime']:
            from src.Entities.FullTimeStudent import FullTimeStudent
            student = FullTimeStudent(user)
        else:
            from src.Entities.PartTimeStudent import PartTimeStudent
            student = PartTimeStudent(user)

        student.exp_grad_date = student_data['expected_graduation']
        student.major = student_data['major']

        # TODO move these to a separate function so they can be
        # lazy loaded
        restrictions = self.db_helper.load_student_restrictions(
            student.user_data.id)

        restrictions = [RESTRICTION_MAPPER[r] for r in restrictions]
        student.restrictions = restrictions

        return student

    def load_current_courses(self, student: Student):
        print("load enrollments called from student mapper")
        db_helper = DatabaseHelper.getInstance()
        loaded_data = db_helper.load_current_enrollment_by_student_id(
            student.user_data.id)
        print("loaded data from load_current_courses", loaded_data)
        course_section_factory = CourseSectionFactory.getInstance()
        course_sections = course_section_factory.build_course_sections(
            loaded_data)
        return course_sections

        # loaded_data = db_helper.load_current_enrollment_by_student_id(
        #     student.user_data.id)
        # print("loaded data from student mapper:", loaded_data)
        # enrollment_factory = EnrollmentFactory.getInstance()
        # enrollments = enrollment_factory.build_enrollments(loaded_data)
        # print("enrollments from student mapper", enrollments)
        # return enrollments

    def load_course_history(self, student: Student):
        from src.Entities.Student import Student
        print("load course history called from student mapper")
        db_helper = DatabaseHelper.getInstance()
        loaded_data = db_helper.load_enrollment_history_by_student_id(
            student.user_data.id)
        print("loaded data from student mapper:", loaded_data)
        enrollment_factory = EnrollmentFactory.getInstance()
        enrollments = enrollment_factory.build_enrollments(loaded_data)
        print("enrollments from student mapper", enrollments)
        return enrollments

    def save(self):
        pass
