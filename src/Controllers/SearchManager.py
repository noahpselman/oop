from src.Factories.CourseSectionFactory import CourseSectionFactory
from src.Database.DatabaseHelper import DatabaseHelper


class SearchManager():
    """
    returns requested list course_sections to caller



    TODO
    add options for filtering results based on student data
    (ie times of current courses)
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if SearchManager.__instance == None:
            SearchManager()
        return SearchManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if SearchManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            SearchManager.__instance = self

    def execute(self, search_dict):
        """
        search_dict has atleast one of the keys:
            'department': str
            'course_number'str
            'instructor'str
        """

        db_helper = DatabaseHelper.getInstance()
        result = db_helper.search_course_sections(search_dict)
        factory = CourseSectionFactory.getInstance()
        course_sections = factory.build_course_sections(result)

        return course_sections
