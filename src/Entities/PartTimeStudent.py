

from src.Entities.Student import Student



class PartTimeStudent(Student):
    def __init__(self, user_data):
        super().__init__(user_data)

        self._maximum_enrollment = 2

    @property
    def maximum_enrollment(self):
        return self._maximum_enrollment

    @maximum_enrollment.setter
    def maximum_enrollment(self, new_maximum_enrollment):
        self._maximum_enrollment = new_maximum_enrollment