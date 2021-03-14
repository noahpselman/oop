from src.Database.DatabaseHelper import DatabaseHelper


class QueryObject():

    def __init__(self, search_dict) -> None:
        """
        search_dict has atleast one of the keys:
            'department': str
            'course_number': str
            'instructor': str
            'quarter': str

        note: current implementation only works because search
        criteria has just one value
        if users could search multiple departments, for example,
        this would have to be adjusted
        to leave flexibility i'm storing the full dictionary and the
        keys as attributes even though the latter is currently
        necessary
        """
        self.search_dict = search_dict
        self.department = search_dict.get('deparment', None)
        self.course_id = search_dict.get('course_id', None)
        self.instructor = search_dict.get('instructor', None)

    def translate(self):
        query = f"""
        SELECT course_id, department, section_number
        FROM course_section
        WHERE {self.build_filter()}
        """
        return query

    def build_filter(self):
        filters = [f'{k} = {v}' for k, v in self.search_dict.items()]
        return ' AND '.join(filters)

    def execute(self):
        query = self.translate()
        db_helper = DatabaseHelper.getInstance()
        result = db_helper.search_course_sections(query)
        return result
