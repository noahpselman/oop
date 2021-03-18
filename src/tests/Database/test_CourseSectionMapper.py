from src.Database.CourseSectionMapper import CourseSectionMapper
import pytest
from unittest.mock import Mock


def test_load():
    course_id = "241"
    department = "POTS"
    quarter = "WINTER 2021"
    section_number = "0"
    mapper = CourseSectionMapper.getInstance()
    result = mapper.load(course_id=course_id, section_number=section_number,
                         department=department, quarter=quarter)
    assert type(result) == dict


def test_get_enrollment_total():
    course_id = "241"
    department = "POTS"
    quarter = "WINTER 2021"
    section_number = "0"
    mapper = CourseSectionMapper.getInstance()
    result = mapper.get_enrollment_total(course_id=course_id, section_number=section_number,
                                         department=department, quarter=quarter)
    assert type(result) == int
