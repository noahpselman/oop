import pytest
from unittest.mock import Mock
from src.Validations.AlreadyInCourseValidation import AlreadyInCourseValidation


def test_is_valid_true():
    report = Mock()
    student = Mock()
    course_1 = Mock()
    course_2 = Mock()
    course_1.course_section_name = 'a'
    course_2.course_section_name = 'b'
    student.get_courses_by_quarter.return_value = [course_1, course_2]
    course_section = Mock()
    course_section.course_section_name = 'b'
    v = AlreadyInCourseValidation.getInstance()
    v.is_valid(report, course_section=course_section, student=student)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=True, msg="You are already enrolled in this course")


def test_is_valid_false():
    report = Mock()
    student = Mock()
    course_1 = Mock()
    course_2 = Mock()
    course_1.course_section_name = 'a'
    course_2.course_section_name = 'b'
    student.get_courses_by_quarter.return_value = [course_1, course_2]
    course_section = Mock()
    course_section.course_section_name = 'c'
    v = AlreadyInCourseValidation.getInstance()
    v.is_valid(report, course_section=course_section, student=student)
    report.add_data.assert_called_once_with(validation=v.__class__.__name__,
                                            success=False, msg="You're not already enrolled in this course")
