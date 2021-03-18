from src.Database.EnrollmentObjectMapper import EnrollmentObjectMapper
import pytest
from unittest.mock import Mock, patch
# import src.Database.DatabaseHelper as DatabaseHelperFile
from src.Database.DatabaseHelper import DatabaseHelper


# Everything here has been tested in other classes
# This suggests my design can be improved
# @patch('__main__.DatabaseHelper', 'getInstance', autospec=True)
@patch('__main__.DatabaseHelper', 'getInstance', autospec=True)
def test_insert():
    enrollable = Mock()
    enrollable.section_number = 0
    enrollable.course_id = 241
    enrollable.department = 'POTS'
    enrollable.student_id = 178
    db_helper = Mock()
    db_helper.insert.return_value = True
    DatabaseHelper.getInstance.return_value = db_helper
    mapper = EnrollmentObjectMapper.getInstance()
    rv = mapper.insert(enrollable)
    assert rv == True
