import pytest
from unittest.mock import Mock
from src.Validations.CourseHasEmptySeatValidation import CourseHasEmptySeatValidation


def test_is_valid_true():
    report = Mock()
    course_section = Mock()
    course_section.get_enrollment_total.return_value = 5
    course_section.capacity = 10

    v = CourseHasEmptySeatValidation.getInstance()
    v.is_valid(report, course_section=course_section)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=True, msg="Course has an open seat")


def test_is_valid_false():
    report = Mock()
    course_section = Mock()
    course_section.get_enrollment_total.return_value = 10
    course_section.capacity = 10

    v = CourseHasEmptySeatValidation.getInstance()
    v.is_valid(report, course_section=course_section)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=False, msg="Course is full")
