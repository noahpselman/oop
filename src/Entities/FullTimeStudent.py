
from src.Entities.Student import Student


class FullTimeStudent(Student):

    def __init__(self, user_data):
        super().__init__(user_data)

        self._max_enrollment = 3

    @property
    def max_enrollment(self):
        return self._max_enrollment

    @max_enrollment.setter
    def max_enrollment(self, new_max_enrollment):
        self._max_enrollment = new_max_enrollment
