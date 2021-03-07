from __future__ import annotations
from src.Factories.EnrollmentFactory import EnrollmentFactory
from src.Database.Mapper import Mapper
from typing import List
# from src.classes.UserMainController import StudentMainController
from src.Database.StudentMapper import StudentMapper

# from src.classes.CourseSection import CourseSection
# from src.classes.StudentState import *
# from src.classes.User import User


class Student():

    # def __init__(self, university_id: str, name: str) -> None:
    #     super().__init__(university_id, name)

    def __init__(self, user_data: User):
        """
        should I inject the mapper dependency
        """
        # self._state = OpenStudentState(self)
        self._user_data: User = user_data
        self._exp_grad_date: str = None
        self._major: str = None
        self._course_history = []
        self._restrictions: List[Restriction] = []
        self._current_courses = []

        # self._controller = StudentMainController.get_instance()

        # self._load()
        # self.transition_to(OpenStudentState(self))

    # course history could be stored as a list of
    # strings of course_ids or course participation
    # objects - will need to weigh the pros/cons

    def __repr__(self):
        return f"""Student {self.user_data.id} with major {self.major}"""

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
        """
        TODO check major is a department
        """
        self._major = new_major

    @property
    def restrictions(self):
        return self._restrictions

    @restrictions.setter
    def restrictions(self, new_restrictions):
        self._restrictions = new_restrictions

    @property
    def course_history(self):
        print("course history getter called from student")
        if not self._course_history:
            self.__load_course_history()
        return self._course_history

    def __load_course_history(self):
        print("loading historic courses in student")
        mapper = StudentMapper.getInstance()
        enrollments = mapper.load_course_history(self)
        self._course_history = enrollments

    @property
    def current_courses(self):
        print("current courses getter called from student")
        if not self._current_courses:
            self.__load_current_courses()
        return self._current_courses

    def __load_current_courses(self):
        print("loading current courses in student")
        mapper = StudentMapper.getInstance()
        current_courses = mapper.load_current_courses(self)
        self._current_courses = current_courses
        # enrollment_factory = EnrollmentFactory.getInstance()
        # enrollment_factory.build(self)

    def add_current_course(self, new_current_course):
        curr_courses = self.current_courses
        if len(curr_courses) >= self.maximum_enrollment:
            raise StudentFullCourseloadException

    @property
    def user_data(self):
        return self._user_data

    def id(self):
        return self.user_data.id

    def email(self):
        return self.user_data.email

    def register_for_course(self, registrar: Registrar, course_section: CourseSection):
        return self._state.register_for_course(registrar, course_section)

    def make_request(self, request_policy: RequestPolicy, course_section: CourseSection):
        return self._state.make_request(request_policy, course_section)

    def jsonify(self):
        result = {
            "user_data": self.user_data.jsonify(),
            "exp_grad_date": self.exp_grad_date,
            "major": self.major,
            "course_history": [c.jsonify() for c in self.course_history],
            "restrictions": [r.jsonify() for r in self.restrictions],
            "current_courses": [c.jsonify() for c in self.current_courses]
        }
        return result

    # def _load(self):
    #     print("student calling load")
    #     mapper = StudentMapper.getInstance()
    #     mapper.load(self)
