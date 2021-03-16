from src.Database.SQLDatabase import SQLDatabase
import pytest


def test_find_all():

    # setup
    tables = ["users", "course_section"]
    on = {
        "users": {
            "university_id": {
                "course_section": "instructor_id"
            }
        }
    }

    select = {
        "users": ["name"],
        "course_section": ["course_id", "section_number"]
    }

    filter = {
        "users": {
            "university_id": {"value": 37, "op": "="}
        },
        "course_section": {
            "quarter": {"value": "SPRING 2021", "op": "="}
        }
    }

    db = SQLDatabase.getInstance()
    result = db.find_all(select, tables, filter=filter, on=on)
    assert result
    assert len(result) == 2
    print(list(result[0]))
    assert list(result[0]) == ['Rolanda Hooch', 340, 0]


def test_find_one():

    # setup
    tables = ["users", "course_section"]
    on = {
        "users": {
            "university_id": {
                "course_section": "instructor_id"
            }
        }
    }

    select = {
        "users": ["name"],
        "course_section": ["course_id", "section_number"]
    }

    filter = {
        "users": {
            "university_id": {"value": 37, "op": "="}
        },
        "course_section": {
            "quarter": {"value": "SPRING 2021", "op": "="}
        }
    }

    db = SQLDatabase.getInstance()
    result = db.find_one(select, tables, filter=filter, on=on)
    assert result
    assert list(result) == ['Rolanda Hooch', 340, 0]
