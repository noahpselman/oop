from __future__ import annotations
import psycopg2

from src.util import get_current_quarter, get_past_quarters


class Database:

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Database.__instance == None:
            Database()
        return Database.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if Database.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, new_conn):
        self._conn = new_conn

    def load_user_by_id(self, university_id):
        query = """
        SELECT university_id, name, email, user_type
        FROM users
        WHERE university_id = %s
        """
        return self.fetch_one(query, (university_id,))

    def load_student_by_id(self, university_id):
        query = """
        SELECT  *
        FROM student
        WHERE university_id = %s
        """
        return self.fetch_one(query, (university_id,))
        # cur = self.conn.cursor()
        # cur.execute(query, (university_id,))
        # return cur.fetchone()

    def fetch_one(self, query, args):
        cur = self.conn.cursor()
        cur.execute(query, args)
        return cur.fetchone()

    def fetch_all(self, query, args):
        cur = self.conn.cursor()
        cur.execute(query, args)
        return cur.fetchall()

    def load_student_restrictions(self, university_id):
        query = """
        SELECT restriction FROM student_restrictions
        WHERE university_id = %s
        """
        return self.fetch_all(query, (university_id,))

    def load_current_enrollment_by_student_id(self, student_id: str):
        query = """
        SELECT section_number, course_id, department,
        quarter, student_id, type
        FROM enrollment
        WHERE student_id = %s AND quarter = %s
        """
        return self.fetch_all(query, (student_id, get_current_quarter()))

    def load_enrollment_history_by_student_id(self, student_id: str):
        query = """
        SELECT section_number, course_id, department,
        quarter, student_id, type
        FROM enrollment
        WHERE student_id = %s AND quarter in %s
        """
        return self.fetch_all(query, (student_id, get_past_quarters()))

    def get_current_quarter(self, today: datetime.date):
        query = """
        SELECT name, start_date, end_date
        FROM quarter
        WHERE start_date < %s AND end_date >= %s
        """
        return self.fetch_one(query, (today, today))

    def get_past_quarters(self, today: datetime.date):
        query = """
        SELECT name, start_date, end_date
        FROM quarter
        WHERE end_date < %s
        """
        return self.fetch_all(query, (today,))


STUDENT_TABLE_NAMES = {
    "STUDENT_TABLE_NAME": "student",
    "STUDENT_PK": "university_id",
    "STUDENT_COLUMN_EXPECTED_GRADUATION": "expected_graduation",
    "STUDENT_COLUMN_MAJOR": "major",
    "STUDENT_COLUMN_FULLTIME": "maximum_enrollment"
}