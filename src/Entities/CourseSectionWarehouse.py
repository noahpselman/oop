class CourseSectionWarehouse():

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CourseSectionWarehouse.__instance == None:
            CourseSectionWarehouse()
        return CourseSectionWarehouse.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if CourseSectionWarehouse.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CourseSectionWarehouse.__instance = self