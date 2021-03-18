import pytest
from unittest.mock import Mock
from src.Validations.OverloadPermissionValidation import OverloadPermissionValidation


def test_is_valid_true():
    report = Mock()
    student = Mock()
    student.max_enrollment = 3
    student.current_courses = ['blah', 'blah']

    v = OverloadPermissionValidation.getInstance()
    v.is_valid(report, student=student)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=True, msg="You will not exceed your maximum number of enrolled courses")


def test_is_valid_false():
    report = Mock()
    student = Mock()
    student.max_enrollment = 3
    student.current_courses = ['blah', 'blah', 'blah']

    v = OverloadPermissionValidation.getInstance()
    v.is_valid(report, student=student)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=False, msg="You are at your maximum enrollment.  An overload request " +
        "from your department head is required.")
