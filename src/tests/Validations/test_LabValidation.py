import pytest
from unittest.mock import Mock
from src.Validations.LabValidation import LabValidation


def test_is_valid_true():
    report = Mock()
    course_section = Mock()
    course_section.lab.course_info = 'a'

    student = Mock()
    course1 = Mock()
    course1.course_info = 'b'
    course2 = Mock()
    course2.course_info = 'a'

    student.get_courses_by_quarter.return_value = [course1, course2]

    v = LabValidation.getInstance()
    v.is_valid(report, student=student, course_section=course_section)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=True, msg="You are enrolled in the lab")


def test_is_valid_false():
    report = Mock()
    course_section = Mock()
    # course_section.lab.__repr__ = 'a'
    course_section.lab.course_info = 'a'

    student = Mock()
    course1 = Mock()
    course1.course_info = 'b'
    course2 = Mock()
    course2.course_info = 'c'

    student.get_courses_by_quarter.return_value = [course1, course2]

    v = LabValidation.getInstance()
    v.is_valid(report, student=student, course_section=course_section)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=False, msg=f"You are not enrolled in the lab: {course_section.lab}")
