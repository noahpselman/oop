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
    def user_data(self):
        return self._user_data

    @property
    def department(self):
        return self._department

    def jsonify(self):
        return {
            'user_data': self.user_data.jsonify(),
            'department': self.department
        }

    def __repr__(self):
        return f"Instructor {self.user_data} in {self.department}"