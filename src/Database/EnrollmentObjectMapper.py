from __future__ import annotations

from src.Database.DatabaseHelper import DatabaseHelper
from src.Database.Mapper import Mapper
from src.Entities.EnrollmentObject import EnrollmentObject


class EnrollmentObjectMapper(Mapper):
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if EnrollmentObjectMapper.__instance == None:
            EnrollmentObjectMapper()
        return EnrollmentObjectMapper.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if EnrollmentObjectMapper.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            EnrollmentObjectMapper.__instance = self
        super().__init__()

    def save(self):
        pass

    def load(self, id: str):

        db_helper = DatabaseHelper.getInstance()
        return db_helper.load_enrollment_history_by_student_id(id)

    def insert(self, enrollable: Enrollable):
        """
        Enrollable is anything that responds to the messages
        in this method
        """

        new_enrollment_kwargs = {
            'section_number': enrollable.section_number,
            'course_id': enrollable.course_id,
            'department': enrollable.department,
            'quarter': enrollable.quarter,
            'student_id': enrollable.student_id,
            'state': enrollable.state,
            'type': 'REGULAR'
        }

        db_helper = DatabaseHelper.getInstance()
        return db_helper.insert_new_enrollment(new_enrollment_kwargs)
