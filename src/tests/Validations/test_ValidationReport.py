import pytest
from unittest.mock import Mock
from src.Validations.ValidationReport import ValidationReport


def test_add_data_true():
    validation_report = ValidationReport()
    validation = Mock()
    success = True
    msg = "msg"
    validation_report.add_data(validation=validation, success=success, msg=msg)
    result = {
        'data': {validation: {'success': True, 'msg': 'msg'}},
        'fails': [],
        'success': True,
        'db_updated': False,
        'msgs': []
    }

    assert result == validation_report.jsonify()


def test_add_data_false():
    validation_report = ValidationReport()
    validation = Mock()
    success = False
    msg = "msg"
    validation_report.add_data(validation=validation, success=success, msg=msg)
    result = {
        'data': {validation: {'success': False, 'msg': 'msg'}},
        'fails': [validation],
        'success': False,
        'db_updated': False,
        'msgs': ['msg']
    }

    assert result == validation_report.jsonify()
