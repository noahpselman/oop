from __future__ import annotations

from src.Entities.Instructor import Instructor
from src.Database.DatabaseHelper import DatabaseHelper
from src.Database.Mapper import Mapper


class InstructorMapper(Mapper):

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if InstructorMapper.__instance == None:
            InstructorMapper()
        return InstructorMapper.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if InstructorMapper.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            InstructorMapper.__instance = self
            super().__init__()

    def load(self, user: User):
        db_helper = DatabaseHelper.getInstance()
        instructor_data = db_helper.load_instructor_by_id(user.id)
        instructor = Instructor(
            user_data=user, department=instructor_data['department'])
        return instructor

    def save(self):
        pass
