from src.util import make_course_index
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
        prereqs = self.__load_prereqs(kwargs['course_id'])
        loaded_data['prereqs'] = prereqs
        course = Course(**loaded_data)
        return course

    def __load_prereqs(self, course_id: str):
        db_helper = DatabaseHelper.getInstance()
        loaded_data = db_helper.load_prereqs_by_course_id(course_id)
        prereqs = []
        for d in loaded_data:
            prereq = make_course_index(
                course_id=d['prereq_id'], department=d['prereq_department'])
            prereqs.append(prereq)
        return prereqs

    def save(self):
        pass
