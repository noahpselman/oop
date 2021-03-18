import pytest
from unittest.mock import Mock
from src.Validations.CourseHasNotFinishedValidation import CourseHasNotFinishedValidation


def test_is_valid_true():
    report = Mock()
    course_section = Mock()
    course_section.state = "PRESTART"

    v = CourseHasNotFinishedValidation.getInstance()
    v.is_valid(report, course_section=course_section)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=True, msg="Course is has not started and can be dropped")


def test_is_valid_false():
    report = Mock()
    course_section = Mock()
    course_section.state = "FINISHED"

    v = CourseHasNotFinishedValidation.getInstance()
    v.is_valid(report, course_section=course_section)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=False, msg="Course is has started and cannot be dropped")
