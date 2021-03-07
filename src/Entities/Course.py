class Course():
    def __init__(self, **kwargs) -> None:
        self._course_id = kwargs['course_id']
        self._name = kwargs['name']
        self._department = kwargs['department']

    @property
    def course_id(self):
        return self._course_id

    @property
    def name(self):
        return self._name

    @property
    def department(self):
        return self._department

    def course_info(self):
        return f"{self.department} {self.course_id}"

    def __repr__(self):
        return self.name + " " + self.course_info()

    def jsonify(self):
        return self.__dict__
