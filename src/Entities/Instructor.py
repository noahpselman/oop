from __future__ import annotations

from src.Entities.User import User


class Instructor():

    def __init__(self, *, user_data, department) -> None:
        """
        kwargs are as seen in constructor
        user_data is a user object created in instructor mapper
        """
        self._user_data: User = user_data
        self._department: str = department

    @property
    def email(self):
        return self._user_data.email

    @property
    def department(self):
        return self._department

    def jsonify(self):
        return {
            'user_data': self._user_data.jsonify(),
            'department': self.department
        }

    def __repr__(self):
        return f"Instructor {self._user_data} in {self.department}"
