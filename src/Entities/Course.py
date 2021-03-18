

from src.util import make_course_index


class Course():
    """
    responsibility is to hold data relevant to specific courses
    (particularly data that may need to be checked by the reg
    process)

    courses are almost always held by course section objects
    """

    def __init__(self, *, course_id: str, name: str, department: str, **kwargs) -> None:
        self._course_id = course_id
        self._name = name
        self._department = department
        self._prereqs = kwargs.get('prereqs', [])
        self._is_lab = kwargs['is_lab']
        self._lab: Course = kwargs.get('lab', None)
        self._has_lab = bool(self._lab)

    @property
    def has_lab(self):
        return self._has_lab

    @property
    def lab(self):
        return self._lab

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

    @property
    def course_info(self):
        """
        makes familiar string of course indentification
        information
        """
        return make_course_index(course_id=self.course_id, department=self.department)

    def __repr__(self):
        return self.name + " " + self.course_info

    def jsonify(self):
        result = {
            'name': self.name,
            'course_id': self.course_id,
            'department': self.department,
            'prereqs': self.prereqs,
            'course_index': self.course_info
        }
        return result
