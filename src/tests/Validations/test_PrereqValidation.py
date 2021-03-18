import pytest
from unittest.mock import Mock
from src.Validations.PrereqValidation import PrereqValidation


def test_is_valid_true():
    report = Mock()
    course_section = Mock()
    prereq1 = 'a'
    prereq2 = 'b'
    course_section.prereqs = [prereq1, prereq2]

    course1 = Mock()
    course1.course_index = 'a'
    course2 = Mock()
    course2.course_index = 'b'
    student = Mock()
    student.course_history = [course1, course2]

    v = PrereqValidation.getInstance()
    v.is_valid(report, student=student, course_section=course_section)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=True, msg="You have met all the prereqs")


def test_is_valid_false():
    report = Mock()
    course_section = Mock()
    prereq1 = 'a'
    prereq2 = 'b'
    course_section.prereqs = [prereq1, prereq2]

    course1 = Mock()
    course1.course_index = 'a'
    course2 = Mock()
    course2.course_index = 'c'
    student = Mock()
    student.course_history = [course1, course2]

    v = PrereqValidation.getInstance()
    v.is_valid(report, student=student, course_section=course_section)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=False, msg="You have not completed the following prereqs: b")
