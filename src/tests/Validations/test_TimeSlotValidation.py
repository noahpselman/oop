import pytest
from unittest.mock import Mock
from src.Validations.TimeSlotValidation import TimeSlotValidation


def test_is_valid_true():
    report = Mock()
    course_section = Mock()
    prereq1 = 'a'
    prereq2 = 'b'
    course_section.prereqs = [prereq1, prereq2]

    course1 = Mock()
    course1.course_section_name = 'a'
    course1.timeslot.no_overlap.return_value = True
    course2 = Mock()
    course2.course_section_name = 'b'
    course2.timeslot.no_overlap.return_value = True
    student = Mock()
    student.get_courses_by_quarter.return_value = [course1, course2]

    v = TimeSlotValidation.getInstance()
    v.is_valid(report, student=student, course_section=course_section)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=True, msg="You have no time conflicts")


def test_is_valid_false():
    report = Mock()
    course_section = Mock()
    prereq1 = 'a'
    prereq2 = 'b'
    course_section.prereqs = [prereq1, prereq2]

    course1 = Mock()
    course1.course_section_name = 'a'
    course1.timeslot.no_overlap.return_value = False
    course2 = Mock()
    course2.course_section_name = 'b'
    course2.timeslot.no_overlap.return_value = True
    student = Mock()
    student.get_courses_by_quarter.return_value = [course1, course2]

    v = TimeSlotValidation.getInstance()
    v.is_valid(report, student=student, course_section=course_section)
    report.add_data.assert_called_once_with(
        validation=v.__class__.__name__, success=False, msg="The following coures are causing time conflicts: a")
