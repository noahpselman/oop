
"""
handles all database requests
"""

from datetime import datetime
from src.util import get_current_quarter
from typing import List
from src.Database.Database import Database


LOAD_STUDENT_COLUMNS = (["university_id", "expected_graduation",
                         "major", "fulltime", "maximum_enrollment"])

LOAD_USER_COLUMNS = (["university_id", "name", "email", "user_type"])

LOAD_ENROLLMENT_COLUMNS = (["section_number", "course_id", "department",
                            "quarter", "student_id", "type", "state"])

LOAD_QUARTER_COLUMNS = (["name", "start_date", "end_date"])

LOAD_COURSE_COLUMNS = (["course_id", "department", "name", "is_lab", "lab_id"])

LOAD_COURSE_SECTION_COLUMNS = (["section_number", "department", "course_id",
                                "quarter", "timeslot", "enrollment_open", "state",
                                "instructor_id", "capacity", "instructor_permission_required"])

LOAD_INSTRUCTOR_COLUMNS = (["university_id", "department"])

LOAD_TIMESLOT_COLUMNS = (["days", "starttime", "endtime"])

LOAD_PREREQ_COLUMNS = (['course_id', 'course_department',
                        'prereq_id', 'prereq_department'])

SEARCH_COURSE_SECTION_COLUMNS = (['course_id', 'department',
                                  'section_number', 'quarter'])


class DatabaseHelper():

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DatabaseHelper.__instance == None:
            DatabaseHelper()
        return DatabaseHelper.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if DatabaseHelper.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseHelper.__instance = self
        self.db = Database.getInstance()
        if not self.db.conn:
            raise Exception("Database doesn't have connection")

    def unpack_db_result(self, columns: tuple, result):
        """
        creates dictionary from db results
        columns: tuple containing names of columns
        result: result of fetch_one from db class
        """
        # return {col: result[col] for col in columns}
        result_dict = {}
        for col in columns:
            result_dict[col] = result[col]
        return result_dict

    def load_user_by_id(self, university_id: str):
        result = self.db.load_user_by_id(university_id)
        return self.unpack_db_result(LOAD_USER_COLUMNS, result)

    def load_student_by_id(self, university_id: str) -> dict:
        """
        queries db and formats result into dict with
        table colnames as keys and values as values
        """
        # result_dict = {}
        print("db-helper loading student")
        result = self.db.load_student_by_id(university_id)
        return self.unpack_db_result(LOAD_STUDENT_COLUMNS, result)
        # for col in LOAD_STUDENT_COLUMNS:
        #     result_dict[col] = result[col]
        # print("result_dict from dbhelper", result_dict)
        # return result_dict

    def load_student_restrictions(self, univeristy_id: str) -> List[str]:
        result_list = []
        result = self.db.load_student_restrictions(univeristy_id)
        print("restrictions from db helper", result)
        for row in result:
            result_list.append(row[0])
        print("result list", result_list)
        return result_list
        # for col in LOAD_STUDENT_COLUMNS:
        #     result_dict[col] = result[col]
        # return result_dict

    def load_enrollment_by_student_quarter(self, student_id: str, quarter: str):
        print("load enrollment by student id called from db helper")
        result = self.db.load_enrollment_by_student_quarter(
            student_id, quarter)
        result_list = [self.unpack_db_result(
            LOAD_ENROLLMENT_COLUMNS, r) for r in result]
        return result_list

    def load_timeslots_by_student_quarter(self, student_id: str, quarter: str):
        print("load enrollement by student quarter classed")
        result = self.db.load_timeslots_by_student_quarter(
            student_id, quarter)
        result_list = [self.unpack_db_result(
            LOAD_ENROLLMENT_COLUMNS, r) for r in result]
        return result_list

    def load_enrollment_history_by_student_id(self, student_id: str):
        print("load enrollment history by student id called from db helper")
        result = self.db.load_enrollment_history_by_student_id(student_id)
        result_list = [self.unpack_db_result(
            LOAD_ENROLLMENT_COLUMNS, r) for r in result]
        return result_list

    def get_current_quarter(self, today: datetime.date):
        result = self.db.get_current_quarter(today)
        return self.unpack_db_result(LOAD_QUARTER_COLUMNS, result)

    def get_past_quarters(self, today: datetime.date):
        result = self.db.get_past_quarters(today)
        # print("result from database helper:", result)
        result_list = [self.unpack_db_result(
            LOAD_QUARTER_COLUMNS, r) for r in result]
        return result_list

    def load_course_by_course_id(self, **kwargs):
        """
        kwargs must include course_id (str) and department (str)
        """
        print("kwargs in load couse by course_id")
        print(kwargs)
        result = self.db.load_course_by_course_id(**kwargs)
        return self.unpack_db_result(LOAD_COURSE_COLUMNS, result)

    def load_instructor_by_id(self, instructor_id: str):
        print("db_helper load instructor arg", instructor_id)
        result = self.db.load_instructor_by_id(instructor_id)
        return self.unpack_db_result(LOAD_INSTRUCTOR_COLUMNS, result)

    def load_timeslot_by_id(self, timeslot_id: str):
        result = self.db.load_timeslot_by_id(timeslot_id)
        return self.unpack_db_result(LOAD_TIMESLOT_COLUMNS, result)

    def load_course_section_by_id(self, **kwargs):
        """
        kwargs must include (all str) course_id, department,
        section_number, quarter
        """
        result = self.db.load_course_section_by_id(**kwargs)
        print("load course section by id from dbhelper", result)
        return self.unpack_db_result(LOAD_COURSE_SECTION_COLUMNS, result)

    def load_prereqs_by_course_id(self, course_id: str):
        result = self.db.load_prereqs_by_course_id(course_id)
        result_list = [self.unpack_db_result(
            LOAD_PREREQ_COLUMNS, r) for r in result]
        return result_list

    def load_enrollment_total_for_course_section(self, **kwargs):
        result = self.db.load_enrollment_total_for_course_section(**kwargs)
        return result[0]

    def insert_new_enrollment(self, enrollment_data: dict):
        """
        enrollment data is should come in as a dict
        """
        print("insert new enrollment called from db helper")
        success = self.db.insert_new_enrollment(enrollment_data)
        print(success)
        return success

    def delete_enrollment(self, **kwargs):
        """
        coming soon
        """
        print("delete enrollment called from db helper")
        success = self.db.delete_enrollment(**kwargs)
        print(success)
        return success

    def search_course_sections(self, search_dict):
        """
        search_dict has the following keys
            'department': str
            'course_number': str
            'instructor': str
            'quarter': str
        """

        colnames = {
            'instructor': 'u.name',
            'department': 'cs.department',
            'section_number': 'cs.section_number',
            'quarter': 'cs.quarter',
            'course_id': 'cs.course_id'
        }

        filters = [f'{colnames[k]} = %s' for k in search_dict.keys()]
        filter_line = ' AND '.join(filters)
        args = tuple(search_dict.values())

        query = f"""
        SELECT course_id, cs.department AS department, section_number, quarter
        FROM course_section cs 
        JOIN users u
        ON cs.instructor_id = u.university_id
        WHERE {filter_line}
        """
        print("query from db helper\n", query)
        print("args", args)
        result = self.db.search_course_sections(query, args)
        result_list = [self.unpack_db_result(
            SEARCH_COURSE_SECTION_COLUMNS, r) for r in result]
        return result_list

    def load_department_email(self, department: str):
        print("load department email called with argument", department)
        result = self.db.load_department_email(department)
        print("load dpearment email result", result)
        return result[0]
