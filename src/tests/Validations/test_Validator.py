import pytest
from unittest.mock import Mock
from src.Validations.Validator import Validator


def test_check_failure():
    fake_validation = Mock()

    validations = [fake_validation]
    report = Mock()
    student = Mock()
    course_section = Mock()

    validator = Validator(student, course_section)

    validator.check_for_failures(validations, report)

    fake_validation.getInstance.assert_called_once
