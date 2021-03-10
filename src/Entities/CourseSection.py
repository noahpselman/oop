from __future__ import annotations

from typing import KeysView
from src.Database.TimeSlotMapper import TimeSlotMapper
from src.Entities.TimeSlot import TimeSlot
from src.util import get_current_quarter, make_section_index


class CourseSection():
    pass
    # def __init__(self) -> None:

    def __init__(self, **kwargs) -> None:
        """
        kwargs are documented in contructor body
        """

        self._section_number: str = kwargs['section_number']
        self._enrollment_open: bool = kwargs['enrollment_open']
        self._course: str = kwargs['course']
        self._quarter: str = kwargs['quarter']
        self._loading_data: dict = kwargs['data']
        self._capacity: int = kwargs['capacity']
        self._state: int = kwargs['state']
        self._instructor_permission_required: bool = kwargs['instructor_permission_required']
        self._instructor: Instructor = None
        self._timeslot: TimeSlot = None
        # instantiating the roster is out of scope of this prototype
        self._roster: List[str] = []

    def get_enrollment_total(self):
        from src.Database.CourseSectionMapper import CourseSectionMapper
        mapper = CourseSectionMapper.getInstance()
        kwargs = {
            'section_number': self.section_number,
            'course_id': self.course_id,
            'department': self.department,
            'quarter': self.quarter
        }
        return mapper.get_enrollment_total(**kwargs)

    @property
    def state(self):
        return self._state

    @property
    def instructor_permission_required(self):
        return self._instructor_permission_required

    @property
    def prereqs(self):
        return self._course.prereqs

    @property
    def course(self):
        return self._course

    @property
    def course_id(self):
        return self.course.course_id

    @property
    def department(self):
        return self.course.department

    @property
    def capacity(self):
        return self._capacity

    @property
    def instructor(self):
        if not self._instructor:
            from src.Factories.UserEntityFactory import UserEntityFactory
            factory = UserEntityFactory.getInstance()
            self._instructor = factory.build_from_id(
                self._loading_data['instructor_id'])
        return self._instructor

    @property
    def section_number(self):
        return self._section_number

    @property
    def quarter(self):
        return self._quarter

    @property
    def timeslot(self):
        if not self._timeslot:
            self.__load_timeslot()
        return self._timeslot

    def __load_timeslot(self):
        mapper = TimeSlotMapper.getInstance()
        self._timeslot = mapper.load(self._loading_data['timeslot_id'])

    @property
    def enrollment_open(self):
        return self._enrollment_open

    @enrollment_open.setter
    def enrollment_open(self, new_enrollment_open):
        self._enrollment_open = new_enrollment_open

    @property
    def course_section_name(self):
        kwargs = {
            'department': self.department,
            'course_id': self.course_id,
            'section_number': self.section_number,
            'quarter': self.quarter
        }
        return make_section_index(**kwargs)

    def __repr__(self):
        return self.course_section_name()

    def jsonify(self):
        result = {
            'section_number': self.section_number,
            'enrollment_open': self.enrollment_open,
            'course': self.course,
            'quarter': self.quarter,
            'capacity': self.capacity,
            'loading_data': self.data,
            'instructor': self.instructor.jsonify(),
            'timeslot': self.timeslot.jsonify()
        }
