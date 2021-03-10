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

    def insert(self, enrollment: EnrollmentObject):
        db_helper = DatabaseHelper.getInstance()
        print(enrollment.__dict__)
        return db_helper.insert_new_enrollment(enrollment)
