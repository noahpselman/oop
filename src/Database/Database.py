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

    # def load_current_courses_for_student(self, student_id):
    #     query = """
    #     SELECT section_number, department, course_id
    #     FROM enrollments
    #     """

    def load_course_by_course_id(self, course_id: str, department: str):
        query = """
        SELECT course_id, department, name
        FROM course
        WHERE course_id = %s AND department = %s
        """
        return self.fetch_one(query, (course_id, department))

    def load_course_section_by_id(self, **kwargs):
        """
        kwargs must include (all str) course_id, department,
        section_number, quarter
        """
        query = """
        SELECT section_number, department, course_id,
        quarter, timeslot, enrollment_open,
        state, instructor_id, capacity
        FROM course_section
        WHERE section_number = %s AND
        department = %s AND
        course_id = %s AND
        quarter = %s
        """
        course_id = kwargs['course_id']
        department = kwargs['department']
        section_number = kwargs['section_number']
        quarter = kwargs['quarter']
        return self.fetch_one(query, (section_number, department, course_id, quarter))

    def load_instructor_by_id(self, instructor_id: str):
        query = """
        SELECT university_id, department
        FROM instructor
        WHERE university_id = %s
        """
        print("instructor id for db", instructor_id)
        return self.fetch_one(query, (instructor_id, ))

    def load_timeslot_by_id(self, timeslot_id: str):
        query = """
        SELECT days, starttime, endtime
        FROM timeslot
        WHERE id = %s
        """
        return self.fetch_one(query, (timeslot_id, ))
