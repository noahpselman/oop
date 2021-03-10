

from src.util import make_course_index


class Course():
    def __init__(self, **kwargs) -> None:
        self._course_id = kwargs['course_id']
        self._name = kwargs['name']
        self._department = kwargs['department']
        self._prereqs = kwargs['prereqs']

    @property
    def course_id(self):
        return self._course_id

    @property
    def name(self):
        return self._name

    @property
    def department(self):
        return self._department

    @property
    def prereqs(self):
        return self._prereqs

    def course_info(self):
        return make_course_index(course_id=self.course_id, department=self.department)

    def __repr__(self):
        return self.name + " " + self.course_info()

    def jsonify(self):
        return self.__dict__
