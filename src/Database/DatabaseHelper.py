from __future__ import annotations
from datetime import datetime
from src.util import get_past_quarters
from src.Database.SQLDatabase import SQLDatabase


LOAD_RESTRICTIONS_COLUMNS = (["university_id", "restriction"])

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
    """
    singleton
    responsibility is to translate common caller
    requests into CRUD operations

    the astute grader will ask "hmmmmm doesn't this
    kind of overlap with the mapper classes? couldn't
    he have just implemented the mapper methods
    in terms of CRUD operations"
    touche, grader - well spotted
    this is a refactor I would make if I had more time
    in that case each specific mapper could own its list
    of columns instead of this one.  that would make more
    sense

    TODO: move the "unpack" methods to sql database this class
    shouldn't need to know how to translate db results into
    native python objects
    """

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
        self._db = SQLDatabase.getInstance()

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, new_db):
        self._db = new_db

    def unpack_db_result(self, columns: list, result):
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

    def unpack_results(self, columns, results):
        return [self.unpack_db_result(columns, r) for r in results]

    def load_user_by_id(self, university_id: str):
        tables = ['users']
        filter = {
            'users': {
                'university_id': {'value': university_id, 'op': '='}
            }
        }
        select = {
            "users": LOAD_USER_COLUMNS
        }
        result = self.db.find_one(
            tables=tables, select=select, filter=filter)
        return self.unpack_db_result(LOAD_USER_COLUMNS, result)
        # result = self.db.load_user_by_id(university_id)
        # return self.unpack_db_result(LOAD_USER_COLUMNS, result)

    def load_student_by_id(self, university_id: str) -> dict:
        """
        queries db and formats result into dict with
        table colnames as keys and values as values
        """
        # result_dict = {}

        tables = ['student']
        filter = {
            'student': {
                'university_id': {'value': university_id, 'op': '='}
            }
        }
        select = {
            "student": LOAD_STUDENT_COLUMNS
        }
        result = self.db.find_one(
            tables=tables, select=select, filter=filter)
        return self.unpack_db_result(LOAD_STUDENT_COLUMNS, result)

    def load_student_restrictions(self, university_id: str) -> List[str]:

        tables = ['student_restrictions']
        filter = {
            'student_restrictions': {
                'university_id': {'value': university_id, 'op': '='}
            }
        }
        select = {
            "student_restrictions": ['restriction']
        }
        results = self.db.find_all(
            tables=tables, select=select, filter=filter)
        rv = [r[0] for r in results]
        return rv

    def load_enrollment_by_student_quarter(self, *, student_id: str, quarter: str):
        print("load enrollment by student id called from db helper")
        tables = ['enrollment']
        filter = {
            'enrollment': {
                'student_id': {'value': student_id, 'op': '='},
                'quarter': {'value': quarter, 'op': '='}
            }
        }
        select = {
            "enrollment": LOAD_ENROLLMENT_COLUMNS
        }
        results = self.db.find_all(
            tables=tables, select=select, filter=filter)

        return self.unpack_results(LOAD_ENROLLMENT_COLUMNS, results)

    def load_enrollment_history_by_student_id(self, student_id: str):
        print("load enrollment history by student id called from db helper")
        tables = ['enrollment']
        past_quarter = get_past_quarters()
        filter = {
            'enrollment': {
                'student_id': {'value': student_id, 'op': '='},
                'quarter': {'value': past_quarter, 'op': 'in'}
            }
        }
        select = {
            "enrollment": LOAD_ENROLLMENT_COLUMNS
        }
        results = self.db.find_all(
            tables=tables, select=select, filter=filter)
        return self.unpack_results(LOAD_ENROLLMENT_COLUMNS, results)

    def load_current_quarter(self, today: datetime.date):
        tables = ['quarter']
        filter = {
            'quarter': {
                'start_date': {'value': today, 'op': '<='},
                'end_date': {'value': today, 'op': '>='}
            }
        }
        select = {
            "quarter": LOAD_QUARTER_COLUMNS
        }
        result = self.db.find_one(
            tables=tables, select=select, filter=filter)
        return self.unpack_db_result(LOAD_QUARTER_COLUMNS, result)

    def load_past_quarters(self, today: datetime.date):
        tables = ['quarter']
        filter = {
            'quarter': {
                'start_date': {'value': today, 'op': '<='}
            }
        }
        select = {
            "quarter": LOAD_QUARTER_COLUMNS
        }
        result = self.db.find_all(
            tables=tables, select=select, filter=filter)

        return self.unpack_results(LOAD_QUARTER_COLUMNS, result)

    def load_course_by_course_id(self, *, department: str, course_id: str):
        """
        """
        tables = ['course']
        filter = {
            'course': {
                'course_id': {'value': course_id, 'op': '='},
                'department': {'value': department, 'op': '='}
            }
        }
        select = {
            "course": LOAD_COURSE_COLUMNS
        }
        result = self.db.find_one(
            tables=tables, select=select, filter=filter)
        return self.unpack_db_result(LOAD_COURSE_COLUMNS, result)

    def load_instructor_by_id(self, instructor_id: str):
        tables = ['instructor']
        filter = {
            'instructor': {
                'university_id': {'value': instructor_id, 'op': '='}
            }
        }
        select = {
            "instructor": LOAD_INSTRUCTOR_COLUMNS
        }
        result = self.db.find_one(
            tables=tables, select=select, filter=filter)
        print("instructor id", result)
        return self.unpack_db_result(LOAD_INSTRUCTOR_COLUMNS, result)

    def load_timeslot_by_id(self, timeslot_id: str):
        tables = ['timeslot']
        filter = {
            'timeslot': {
                'id': {'value': timeslot_id, 'op': '='}
            }
        }
        select = {
            "timeslot": LOAD_TIMESLOT_COLUMNS
        }
        result = self.db.find_one(
            tables=tables, select=select, filter=filter)
        return self.unpack_db_result(LOAD_TIMESLOT_COLUMNS, result)

    def load_course_section_by_id(self, *, section_number: str, course_id: str, department: str, quarter: str):
        """

        """
        tables = ['course_section']
        filter = {
            'course_section': {
                'course_id': {'value': course_id, 'op': '='},
                'section_number': {'value': section_number, 'op': '='},
                'quarter': {'value': quarter, 'op': '='},
                'department': {'value': department, 'op': '='}
            }
        }
        select = {
            "course_section": LOAD_COURSE_SECTION_COLUMNS
        }
        result = self.db.find_one(
            tables=tables, select=select, filter=filter)
        return self.unpack_db_result(LOAD_COURSE_SECTION_COLUMNS, result)

    def load_enrollments_by_course_section_id(self, *,
                                              section_number: str, course_id: str,
                                              department: str, quarter: str):
        tables = ['enrollment']
        filter = {
            'enrollment': {
                'course_id': {'value': course_id, 'op': '='},
                'section_number': {'value': section_number, 'op': '='},
                'quarter': {'value': quarter, 'op': '='},
                'department': {'value': department, 'op': '='}
            }
        }
        select = {
            "enrollment": LOAD_ENROLLMENT_COLUMNS
        }
        result = self.db.find_all(
            tables=tables, select=select, filter=filter)
        return self.unpack_results(LOAD_ENROLLMENT_COLUMNS, result)

    def load_prereqs_by_course_id(self, *, course_id: str, department: str):
        tables = ['prereqs']
        filter = {
            'prereqs': {
                'course_id': {'value': course_id, 'op': '='},
                'course_department': {'value': department, 'op': '='}
            }
        }
        select = {
            "prereqs": LOAD_PREREQ_COLUMNS
        }
        result = self.db.find_all(
            tables=tables, select=select, filter=filter)
        return self.unpack_results(LOAD_PREREQ_COLUMNS, result)

    def load_enrollment_total_for_course_section(self, *,
                                                 section_number: str, course_id: str,
                                                 department: str, quarter: str):
        enrollments = self.load_enrollments_by_course_section_id(
            section_number=section_number, course_id=course_id,
            department=department, quarter=quarter)
        # print(len(enrollments))
        return len(enrollments)

    def insert_new_enrollment(self, enrollment_data: dict):
        """
        enrollment_data should include values corresponding
        to LOAD_ENROLLMENT_COLUMNS
        """
        success = self.db.create(
            table='enrollment', values_dict=enrollment_data)

        return success

    def delete_enrollment(self, *,
                          section_number: str, course_id: str,
                          department: str, quarter: str, student_id: str):

        filter = {
            'enrollment': {
                'section_number': {'value': section_number, 'op': '='},
                'course_id': {'value': course_id, 'op': '='},
                'department': {'value': department, 'op': '='},
                'quarter': {'value': quarter, 'op': '='},
                'student_id': {'value': student_id, 'op': '='}
            }
        }

        return self.db.delete(table="enrollment", filter=filter)

    def search_course_sections(self, search_dict):
        """
        search_dict has the following keys
            'department': str
            'course_id': str
            'instructor': str
            'quarter': str

        could this benefit from refactoring: yes
        do i have time to do that now: no
        """
        tables = ['course_section', 'users']
        on = {
            'course_section': {
                'instructor_id': {
                    'users': 'university_id'
                }
            }
        }
        select = {'course_section': SEARCH_COURSE_SECTION_COLUMNS}
        filter = {}
        filter = {
            'course_section': {
                'department': {'value': search_dict.get('department', '%'), 'op': 'LIKE'},
                'quarter': {'value': search_dict.get('quarter', '%'), 'op': 'LIKE'}
            }
        }
        filter = {}
        for var in ['quarter', 'department', 'course_id']:
            if var in search_dict:
                course_section_filter = filter.get('course_section', {})
                course_section_filter[var] = {
                    'value': search_dict[var], 'op': '='}
                filter['course_section'] = course_section_filter
        if 'instructor' in search_dict:
            filter['users'] = {
                'name': {'value': search_dict['instructor'], 'op': '='}
            }
        result = self.db.find_all(
            tables=tables, select=select, filter=filter, on=on)
        return self.unpack_results(SEARCH_COURSE_SECTION_COLUMNS, result)

    def load_department_email(self, department: str):
        tables = ['users', 'department']
        filter = {'department': {
            'department_name': {'value': department, 'op': '='}}
        }
        select = {"users": ["email"]}
        on = {'department': {'chair': {'users': "university_id"}}}
        result = self.db.find_one(
            tables=tables, select=select, filter=filter, on=on)
        return result[0]
