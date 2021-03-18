from src.Database.InstructorMapper import InstructorMapper
import pytest
from unittest.mock import Mock


def test_load():
    user = Mock()
    user.id = 15
    mapper = InstructorMapper.getInstance()
    rv = mapper.load(user)
    return rv.__class__.__name__ == 'Instructor'
