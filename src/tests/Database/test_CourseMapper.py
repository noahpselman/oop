from src.Database.CourseMapper import CourseMapper
import pytest
from unittest.mock import Mock


def test_load():

    cm = CourseMapper.getInstance()
    course_id = "241"
    department = "POTS"
    cm.__load_lab = Mock()
    rv = cm.load(course_id=course_id, department=department)
    cm.__load_lab.assert_not_called()
    assert rv.__class__.__name__ == 'Course'
