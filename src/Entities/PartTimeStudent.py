

from src.Entities.Student import Student


class PartTimeStudent(Student):
    """
    subclass of student with different max enrollment
    i could have put some if-else logic in the student
    class but... why not make a subclass - it's OOP
    afterall
    """
    def __init__(self, user_data):
        super().__init__(user_data)

        self._max_enrollment = 2

    @property
    def max_enrollment(self):
        return self._max_enrollment

    @max_enrollment.setter
    def max_enrollment(self, new_max_enrollment):
        self._max_enrollment = new_max_enrollment

    def jsonify(self):
        result = super().jsonify()
        result['max_enrollment'] = self.max_enrollment
        return result
