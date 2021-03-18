import pytest
from unittest.mock import Mock
from src.Validations.StudentRestrictionValidation import StudentRestrictionValidation


def test_is_valid_true():
    report = Mock()
    student = Mock()
    student.restrictions = []

    v = StudentRestrictionValidation.getInstance()
    v.is_valid(report, student=student)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=True, msg="You have no restrictions")


def test_is_valid_false():
    report = Mock()
    student = Mock()
    student.restrictions = ['a', 'b']

    v = StudentRestrictionValidation.getInstance()
    v.is_valid(report, student=student)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=False, msg="You have the following restrictions on your account: a, b")
