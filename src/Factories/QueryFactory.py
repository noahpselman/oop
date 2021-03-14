class QueryFactory():
    @staticmethod
    def getInstance():
        """ Static access method. """
        if QueryFactory.__instance == None:
            QueryFactory()
        return QueryFactory.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if QueryFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            QueryFactory.__instance = self

    def build(self, search_dict: dict):
        """
        search_dict has atleast one of the keys:
            'department'
            'course_number'
            'instructor'
        """
        return QueryObject(search_dict)
