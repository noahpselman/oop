from __future__ import annotations

from src.Database.DatabaseHelper import DatabaseHelper
from src.Database.Mapper import Mapper
from src.Entities.EnrollmentObject import EnrollmentObject


class EnrollmentObjectMapper(Mapper):
    """
    singleton
    responsible for calling appropriate methods on database helper
    for enrollment objects
    since enrollment objects just hold data, some methods
    work with anything that is "enrollable", meaning it 
    responsed to the messages required to get the data
    corresponding to the database columns

    on occations, dictionaries are used in lieu of enrollment
    objects when they're just used to identify database rows
    prior to creation or deletion
    """
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

    def load(self, id: str) -> List[EnrollmentObject]:

        db_helper = DatabaseHelper.getInstance()
        return db_helper.load_enrollment_history_by_student_id(id)

    def insert(self, enrollable: Enrollable) -> bool:
        """
        Enrollable is anything that responds to the messages
        in this method
        note: an example of another enrollable object is an
        enrollment request which can be passed to this method
        in the permission request sequence
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

    def delete(self, *, student_id: str, course_id:
               str, department: str, section_number: str,
               quarter: str) -> bool:
        db_helper = DatabaseHelper.getInstance()
        return db_helper.delete_enrollment(student_id=student_id, course_id=course_id,
                                           section_number=section_number, department=department, quarter=quarter)
