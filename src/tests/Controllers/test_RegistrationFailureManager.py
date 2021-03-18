from src.Controllers.RegistrationFailureManager import RegistrationFailureManager
import pytest
from unittest.mock import Mock


def test_execute():
    course_section = Mock()
    report = Mock()
    rfm = RegistrationFailureManager()
    assert True
