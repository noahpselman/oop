
"""
handles all database requests
"""

from datetime import datetime
from typing import List
from src.Database.Database import Database


LOAD_STUDENT_COLUMNS = ("university_id", "expected_graduation",
                        "major", "fulltime", "maximum_enrollment")

LOAD_USER_COLUMNS = ("university_id", "name", "email", "user_type")

LOAD_ENROLLMENT_COLUMNS = ("section_number", "course_id", "department",
                           "quarter", "student_id", "type")

LOAD_QUARTER_COLUMNS = ("name", "start_date", "end_date")

LOAD_COURSE_COLUMNS = ("course_id", "department", "name")

LOAD_COURSE_SECTION_COLUMNS = ("section_number", "department", "course_id",
                               "quarter", "timeslot", "enrollment_open", "state",
                               "instructor_id", "capacity")

LOAD_INSTRUCTOR_COLUMNS = ("university_id", "department")

LOAD_TIMESLOT_COLUMNS = ("days", "starttime", "endtime")


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

    def load_current_enrollment_by_student_id(self, student_id: str):
        print("load enrollment by student id called from db helper")
        result = self.db.load_current_enrollment_by_student_id(student_id)
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
        # print(kwargs)
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
        return self.unpack_db_result(LOAD_COURSE_SECTION_COLUMNS, result)
