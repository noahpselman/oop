import pytest
from src.Database.DatabaseHelper import DatabaseHelper
from src.util import get_current_quarter
from unittest.mock import Mock
from datetime import datetime


def test_load_current_quarter():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    rv = {'name': 'WINTER 2020', 'start_date': "eh", 'end_date': "heh"}
    mock_db.find_one.return_value = rv
    db_helper.db = mock_db
    today = datetime.date(datetime.now())
    args = {
        'tables': ['quarter'],
        'select': {'quarter': ['name', 'start_date', 'end_date']},
        'filter': {'quarter': {
            'start_date': {'value': today, 'op': '<='},
            'end_date': {'value': today, 'op': '>='}
        }
        }
    }
    result = db_helper.load_current_quarter(today)
    mock_db.find_one.assert_called_once_with(**args)


def test_load_past_quarters():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    rv = ([{'name': 'WINTER 2020', 'start_date': "eh", 'end_date': "heh"},
           {'name': 'AUTUMN 2019', 'start_date': "meh", 'end_date': "bleh"},
           {'name': 'SUMMER 20219', 'start_date': "geh", 'end_date': "EGATZ"}])
    mock_db.find_all.return_value = rv
    db_helper.db = mock_db
    today = datetime.date(datetime.now())
    result = db_helper.load_past_quarters(today)
    args = {
        'tables': ['quarter'],
        'select': {'quarter': ['name', 'start_date', 'end_date']},
        'filter': {'quarter': {
            'start_date': {'value': today, 'op': '<='},
        }
        }
    }
    mock_db.find_all.assert_called_once_with(**args)
    assert result == rv


def test_load_user_by_id():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    rv = {'university_id': 1, 'name': 'whatever',
          'email': 'dont matter', 'user_type': 'thats right'}
    mock_db.find_one.return_value = rv
    db_helper.db = mock_db
    result = db_helper.load_user_by_id(38)
    args = {
        'tables': ['users'],
        'select': {'users': ['university_id', 'name', 'email', 'user_type']},
        'filter': {'users': {'university_id': {'value': 38, 'op': '='}}}
    }
    mock_db.find_one.assert_called_once_with(**args)
    assert result == rv


def test_load_student_by_id():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    rv = {'university_id': 2, 'expected_graduation': 4893,
          'major': "farts", 'fulltime': True, 'maximum_enrollment': -4}
    mock_db.find_one.return_value = rv
    db_helper.db = mock_db
    result = db_helper.load_student_by_id(102)
    args = {
        'tables': ['student'],
        'select': {'student': ['university_id', 'expected_graduation', 'major', 'fulltime', 'maximum_enrollment']},
        'filter': {'student': {'university_id': {'value': 102, 'op': '='}}}
    }
    mock_db.find_one.assert_called_once_with(**args)
    assert result == rv


def test_load_student_restriction():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    rv = [['TUITION'], ['LIBRARY']]
    mock_db.find_all.return_value = rv
    db_helper.db = mock_db
    result = db_helper.load_student_restrictions(102)
    args = {
        'tables': ['student_restrictions'],
        'select': {'student_restrictions': ['restriction']},
        'filter': {'student_restrictions': {'university_id': {'value': 102, 'op': '='}}}
    }
    mock_db.find_all.assert_called_once_with(**args)
    assert result == ['TUITION', 'LIBRARY']


def test_load_enrollment_by_student_quarter():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    rv = ([
        {
            'section_number': 5,
            'course_id': 300,
            'department': 'DRUGS',
            'quarter': 'WINTER 9999',
            'student_id': 69,
            'type': 'REGULAR',
            'state': 'COMPLETE'
        },
        {
            'section_number': 6,
            'course_id': 330,
            'department': 'SLEEP',
            'quarter': 'WINTER 9999',
            'student_id': 69,
            'type': 'REGULAR',
            'state': 'COMPLETE'
        }
    ])
    mock_db.find_all.return_value = rv
    db_helper.db = mock_db
    result = db_helper.load_enrollment_by_student_quarter(
        student_id=102, quarter='SPRING 2021')
    args = {
        'tables': ['enrollment'],
        'select': {'enrollment': ["section_number", "course_id", "department", "quarter", "student_id", "type", "state"]},
        'filter': {'enrollment': {
            'student_id': {'value': 102, 'op': '='},
            'quarter': {'value': 'SPRING 2021', 'op': '='}
        }
        }
    }
    mock_db.find_all.assert_called_once_with(**args)
    assert result == rv


# def test_load_enrollment_history_by_student_id():
#     db_helper = DatabaseHelper.getInstance()
#     mock_db = Mock()
#     rv = ([
#         {
#         'section_number': 5,
#         'course_id': 300,
#         'department': 'DRUGS',
#         'quarter': 'WINTER 9999',
#         'student_id': 69,
#         'type': 'REGULAR',
#         'state': 'COMPLETE'
#     },
#     {
#         'section_number': 6,
#         'course_id': 330,
#         'department': 'SLEEP',
#         'quarter': 'WINTER 9999',
#         'student_id': 69,
#         'type': 'REGULAR',
#         'state': 'COMPLETE'
#     }
#         ])
#     mock_db.find_all.return_value = rv
#     db_helper.db = mock_db
#     result = db_helper.load_enrollment_history_by_student_id(student_id=102)
#     past_quarters = get_past_quarters()
#     args = {
#         "tables":['enrollment'],
#         "select":{'enrollment': ["section_number", "course_id", "department", "quarter", "student_id", "type", "state"]},
#         "filter":{'enrollment': {
#             'student_id': {'value': 102, 'op': '='},
#             'quarter': {'value': ('WINTER 2020', 'AUTUMN 2019'), 'op': 'in'}}}
#     }
#     mock_db.find_all.assert_called_once_with(**args)
#     assert result == rv

def test_load_course_by_id():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    rv = {'course_id': 222, 'department': 'NOSE',
          'name': "Noses For Ears", 'is_lab': False, 'lab_id': 223}
    mock_db.find_one.return_value = rv
    db_helper.db = mock_db
    result = db_helper.load_course_by_course_id(
        course_id=340, department='QDTC')
    args = {
        'tables': ['course'],
        'select': {'course': ["course_id", "department", "name", "is_lab", "lab_id"]},
        'filter': {'course': {'course_id': {'value': 340, 'op': '='}, 'department': {'value': 'QDTC', 'op': '='}}
                   }
    }
    mock_db.find_one.assert_called_once_with(**args)
    assert result == rv


def test_instructor_by_id():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    rv = {'university_id': 38, 'department': 'NOSE'}
    mock_db.find_one.return_value = rv
    db_helper.db = mock_db
    result = db_helper.load_instructor_by_id(38)
    args = {
        'tables': ['instructor'],
        'select': {'instructor': ["university_id", "department"]},
        'filter': {'instructor': {'university_id': {'value': 38, 'op': '='}}
                   }
    }
    mock_db.find_one.assert_called_once_with(**args)
    assert result == rv


def test_load_timeslot_by_id():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    rv = {'days': 'TR', 'starttime': 800, 'endtime': 1000}
    mock_db.find_one.return_value = rv
    db_helper.db = mock_db
    result = db_helper.load_timeslot_by_id(4)
    args = {
        'tables': ['timeslot'],
        'select': {'timeslot': ["days", "starttime", "endtime"]},
        'filter': {'timeslot': {'id': {'value': 4, 'op': '='}}
                   }
    }
    mock_db.find_one.assert_called_once_with(**args)
    assert result == rv


def test_load_course_section_by_id():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    rv = {"section_number": 2, "department": "NOSE", "course_id": 800, "quarter": 'SPRING 9999',
          "timeslot": 2, "enrollment_open": True, "state": "COMPLETE", "instructor_id": 23,
          "capacity": 20, "instructor_permission_required": False}
    mock_db.find_one.return_value = rv
    db_helper.db = mock_db
    result = db_helper.load_course_section_by_id(
        section_number=4, course_id=210, department="NOSE", quarter='SPRING 0000')
    args = {
        'tables': ['course_section'],
        'select': {'course_section': ["section_number", "department", "course_id", "quarter", "timeslot", "enrollment_open", "state", "instructor_id", "capacity", "instructor_permission_required"]},
        'filter': {'course_section': {
            'course_id': {'value': 210, 'op': '='},
            'department': {'value': 'NOSE', 'op': '='},
            'quarter': {'value': "SPRING 0000", 'op': '='},
            'section_number': {'value': 4, 'op': '='}
        }
        }
    }
    mock_db.find_one.assert_called_once_with(**args)
    assert result == rv


def test_load_prereqs_by_course_id():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    rv = [{"course_id": 222, "course_department": "NOSE", "prereq_id": 211, "prereq_department": "NOSE"},
          {"course_id": 222, "course_department": "NOSE", "prereq_id": 212, "prereq_department": "NOSE"}]
    mock_db.find_all.return_value = rv
    db_helper.db = mock_db
    result = db_helper.load_prereqs_by_course_id(
        course_id=222, department="BLAH")
    args = {
        'tables': ['prereqs'],
        'select': {'prereqs': ["course_id", "course_department", "prereq_id", "prereq_department"]},
        'filter': {'prereqs': {
            'course_id': {'value': 222, 'op': '='},
            'course_department': {'value': 'BLAH', 'op': '='}
        }
        }
    }
    mock_db.find_all.assert_called_once_with(**args)
    assert result == rv


def test_load_enrollments_by_course_section_id():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    rv = ([
        {
            'section_number': 5,
            'course_id': 300,
            'department': 'DRUGS',
            'quarter': 'WINTER 9999',
            'student_id': 69,
            'type': 'REGULAR',
            'state': 'COMPLETE'
        },
        {
            'section_number': 6,
            'course_id': 330,
            'department': 'SLEEP',
            'quarter': 'WINTER 9999',
            'student_id': 69,
            'type': 'REGULAR',
            'state': 'COMPLETE'
        }
    ])
    mock_db.find_all.return_value = rv
    db_helper.db = mock_db
    result = db_helper.load_enrollments_by_course_section_id(
        section_number=4, course_id=210, department="NOSE", quarter='SPRING 0000')
    args = {
        'tables': ['enrollment'],
        'select': {'enrollment': ["section_number",  "course_id", "department", "quarter", "student_id", "type", "state"]},
        'filter': {'enrollment': {
            'course_id': {'value': 210, 'op': '='},
            'department': {'value': 'NOSE', 'op': '='},
            'quarter': {'value': "SPRING 0000", 'op': '='},
            'section_number': {'value': 4, 'op': '='}
        }
        }
    }
    mock_db.find_all.assert_called_once_with(**args)
    assert result == rv


def test_load_enrollment_total_by_course_section_id():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    rv = ([
        {
            'section_number': 5,
            'course_id': 300,
            'department': 'DRUGS',
            'quarter': 'WINTER 9999',
            'student_id': 69,
            'type': 'REGULAR',
            'state': 'COMPLETE'
        },
        {
            'section_number': 6,
            'course_id': 330,
            'department': 'SLEEP',
            'quarter': 'WINTER 9999',
            'student_id': 69,
            'type': 'REGULAR',
            'state': 'COMPLETE'
        }
    ])
    mock_db.find_all.return_value = rv
    db_helper.db = mock_db
    result = db_helper.load_enrollment_total_for_course_section(
        section_number=4, course_id=210, department="NOSE", quarter='SPRING 0000')

    assert result == 2


def test_search_course_sections():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    rv = [{
        'course_id': 340,
        'department': 'YAWN',
        'section_number': 2,
        'quarter': 'SUMMER 2222'},
        {
        'course_id': 340,
        'department': 'YAWN',
        'section_number': 3,
        'quarter': 'SUMMER 2222'}
    ]
    mock_db.find_all.return_value = rv
    db_helper.db = mock_db
    args = {
        'tables': ['course_section', 'users'],
        'select': {'course_section': ["course_id", "department", "section_number", "quarter"]},
        'filter': {'course_section': {
            'course_id': {'value': 210, 'op': '='},
            'department': {'value': 'YAWN', 'op': '='},
            'quarter': {'value': "SUMMER 2222", 'op': '='}},
            'users': {'name': {'value': 'Prof Name', 'op': '='}}},
        'on': {'course_section': {'instructor_id': {'users': 'university_id'}}}
    }
    search_dict = {
        'department': 'YAWN',
        'quarter': 'SUMMER 2222',
        'course_id': 210,
        'instructor': 'Prof Name'
    }

    result = db_helper.search_course_sections(search_dict)
    mock_db.find_all.assert_called_once_with(**args)
    assert result == rv


def test_load_department_email():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    rv = "the@email.com"
    mock_db.find_one.return_value = [rv]
    db_helper.db = mock_db
    result = db_helper.load_department_email('YAWN')
    args = {
        'tables': ['users', 'department'],
        'select': {'users': ["email"]},
        'filter': {'department': {'department_name': {'value': 'YAWN', 'op': '='}}},
        'on': {'department': {'chair': {'users': "university_id"}}}
    }
    mock_db.find_one.assert_called_once_with(**args)
    assert result == rv


def test_insert_new_enrollment():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    db_helper.db = mock_db
    new_enrollment = {
        'section_number': 1,
        'course_id': 441,
        'department': 'TRFG',
        'quarter': 'WINTER 2021',
        'student_id': 102,
        'type': 'REGULAR',
        'state': 'COMPLETE'
    }
    db_helper.insert_new_enrollment(new_enrollment)
    mock_db.create.assert_called_once_with(
        table='enrollment', values_dict=new_enrollment)


def test_delete_enrollment():
    db_helper = DatabaseHelper.getInstance()
    mock_db = Mock()
    db_helper.db = mock_db
    to_delete = {
        'section_number': 1,
        'course_id': 441,
        'department': 'TRFG',
        'quarter': 'WINTER 2021',
        'student_id': 102
    }
    filter = {
        'enrollment': {
            'section_number': {'value': 1, 'op': '='},
            'course_id': {'value': 441, 'op': '='},
            'department': {'value': 'TRFG', 'op': '='},
            'quarter': {'value': 'WINTER 2021', 'op': '='},
            'student_id': {'value': 102, 'op': '='}
        }}

    db_helper.delete_enrollment(**to_delete)
    mock_db.delete.assert_called_once_with(table='enrollment', filter=filter)
