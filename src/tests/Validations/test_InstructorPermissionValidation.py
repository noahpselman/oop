import pytest
from unittest.mock import Mock
from src.Validations.InstructorPermissionValidation import InstructorPermissionValidation


def test_is_valid_true():
    report = Mock()
    course_section = Mock()
    course_section.instructor_permission_required = False

    v = InstructorPermissionValidation.getInstance()
    v.is_valid(report, course_section=course_section)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=True, msg="Instructor permission is not required for this class")


def test_is_valid_false():
    report = Mock()
    course_section = Mock()
    course_section.instructor_permission_required = True

    v = InstructorPermissionValidation.getInstance()
    v.is_valid(report, course_section=course_section)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=False, msg="Instructor permission is required for this class")
