import pytest
from unittest.mock import Mock
from src.Validations.CourseOpenEnrollmentValidation import CourseOpenEnrollmentValidation


def test_is_valid_true():
    report = Mock()
    course_section = Mock()
    course_section.enrollment_open = True

    v = CourseOpenEnrollmentValidation.getInstance()
    v.is_valid(report, course_section=course_section)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=True, msg="Course is open for enrollment")


def test_is_valid_false():
    report = Mock()
    course_section = Mock()
    course_section.enrollment_open = False

    v = CourseOpenEnrollmentValidation.getInstance()
    v.is_valid(report, course_section=course_section)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=False, msg="Course is not open for enrollment")
