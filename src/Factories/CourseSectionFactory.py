from src.Entities.CourseSectionWarehouse import CourseSectionWarehouse


class CourseSectionFactory():

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CourseSectionFactory.__instance == None:
            CourseSectionFactory()
        return CourseSectionFactory.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if CourseSectionFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CourseSectionFactory.__instance = self

        self.warehouse = CourseSectionWarehouse.getInstance()

    
    # def build(course_section_id):
        

    