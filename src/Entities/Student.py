from __future__ import annotations
from src.util import get_current_quarter
from src.Database.StudentMapper import StudentMapper


class Student():
    """
    responsible for storing data that belongs to student
    relevant for actions like registering for courses
    or making requests

    some attributes are instead properties:
        -restrictions
        -coures_history
        -current_courses

    they are lazily loaded as the property is called
    this ensures the user interface will always display
    the most up-to-date values for these variables

    note the student does not have methods to register
    for courses or make requests itself
    this is because the student object would have the pass
    itself as an argument in either of these methods, as the
    respective controllers need to retrieve idiosyncratic
    information from the student.  it saves a step to just
    have the caller (the main controller) directly pass the
    student to the registrar or permission manager

    there is a jsonify method which creates a json
    object ready to export
    """

    def __init__(self, user_data: User):
        """
        """
        self._user_data: User = user_data
        self._exp_grad_date: str = None
        self._major: str = None

    def __repr__(self):
        return f"""{self.__class__.__name__} {self.user_data.id} with major {self.major}"""

    @property
    def exp_grad_date(self) -> str:
        print("getter called")
        return self._exp_grad_date

    @exp_grad_date.setter
    def exp_grad_date(self, new_exp_grad_date: str) -> None:
        self._exp_grad_date = new_exp_grad_date

    @property
    def student_type(self) -> str:
        return self._student_type

    @student_type.setter
    def student_type(self, new_student_type) -> None:
        assert new_student_type in ("full-time", "part-time")
        if new_student_type == "full-time":
            self.maximum_enrollment = 3
        elif new_student_type == "part-time":
            self.maximum_enrollment = 2
        self._student_type = new_student_type

    @property
    def major(self):
        return self._major

    @major.setter
    def major(self, new_major):
        self._major = new_major

    @property
    def restrictions(self):
        return self.__load_restrictions()

    def __load_restrictions(self):
        mapper = StudentMapper.getInstance()
        restrictions = mapper.load_student_restrictions(self.id)
        return restrictions

    @property
    def course_history(self):
        return self.__load_course_history()

    def __load_course_history(self):
        mapper = StudentMapper.getInstance()
        enrollments = mapper.load_course_history(self.id)
        return enrollments

    @property
    def current_courses(self):
        print("current courses getter called from student")
        courses = self.get_courses_by_quarter(
            get_current_quarter())
        return courses

    def get_courses_by_quarter(self, quarter: str):
        mapper = StudentMapper.getInstance()
        courses = mapper.load_courses_by_quarter(student=self, quarter=quarter)
        return courses

    @property
    def user_data(self):
        return self._user_data

    @property
    def id(self):
        return self.user_data.id

    @property
    def email(self):
        return self.user_data.email

    @property
    def full_name(self):
        return self.user_data.full_name

    # def register_for_course(self, registrar: Registrar, course_section: CourseSection):
    #     return registrar.register_for_course(self, course_section)

    # def make_request(self, request_policy: RequestPolicy, course_section: CourseSection):
    #     return self.make_request(request_policy, course_section)

    def jsonify(self):
        result = {
            "user_data": self.user_data.jsonify(),
            "student_data": {
                "exp_grad_date": self.exp_grad_date,
                "major": self.major
            },
            "course_history": [c.jsonify() for c in self.course_history],
            "restrictions": self.restrictions,
            "current_courses": [c.jsonify() for c in self.current_courses]
        }
        return result
