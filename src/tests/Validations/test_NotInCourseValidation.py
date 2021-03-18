import pytest
from unittest.mock import Mock
from src.Validations.NotInCourseValidation import NotInCourseValidation


def test_is_valid_true():
    report = Mock()
    course_section = Mock()
    course_section.course_section_name = 'a'

    student = Mock()
    course1 = Mock()
    course1.course_section_name = 'b'
    course2 = Mock()
    course2.course_section_name = 'c'

    student.get_courses_by_quarter.return_value = [course1, course2]

    v = NotInCourseValidation.getInstance()
    v.is_valid(report, student=student, course_section=course_section)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=True, msg="You're not already enrolled in this course")


def test_is_valid_false():
    report = Mock()
    course_section = Mock()
    course_section.course_section_name = 'a'

    student = Mock()
    course1 = Mock()
    course1.course_section_name = 'b'
    course2 = Mock()
    course2.course_section_name = 'a'

    student.get_courses_by_quarter.return_value = [course1, course2]

    v = NotInCourseValidation.getInstance()
    v.is_valid(report, student=student, course_section=course_section)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=False, msg="You are already enrolled in this course")
