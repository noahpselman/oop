from src.Entities.Course import Course
from src.Database.Mapper import Mapper
from src.Database.DatabaseHelper import DatabaseHelper


class CourseMapper(Mapper):

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CourseMapper.__instance == None:
            CourseMapper()
        return CourseMapper.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if CourseMapper.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CourseMapper.__instance = self
            super().__init__()

    def load(self, **kwargs):
        db_helper = DatabaseHelper.getInstance()
        loaded_data = db_helper.load_course_by_course_id(**kwargs)
        print(loaded_data)
        course = Course(**loaded_data)
        return course

    def save(self):
        pass
