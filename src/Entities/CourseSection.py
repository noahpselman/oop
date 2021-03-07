from __future__ import annotations
from src.Database.TimeSlotMapper import TimeSlotMapper
from src.Entities.TimeSlot import TimeSlot
from src.util import get_current_quarter


class CourseSection():
    pass
    # def __init__(self) -> None:

    def __init__(self, **kwargs) -> None:
        """
        kwargs are documented in contructor body
        data has two keys 'timeslot_id', 'instructor_id', str, str

        """

        self._section_number: str = kwargs['section_number']
        self._enrollment_open: bool = kwargs['enrollment_open']
        self._course: str = kwargs['course']
        self._quarter: str = kwargs['quarter']
        self._loading_data: dict = kwargs['data']
        self._capacity: int = kwargs['capacity']
        self._instructor: Instructor = None
        self._timeslot: TimeSlot = None
        # instantiating the roster is out of scope of this prototype
        self._roster: List[str] = []

    @property
    def course(self):
        return self._course

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
    def open_enrollment(self):
        return self._open_enrollment

    @open_enrollment.setter
    def open_enrollment(self, new_open_enrollment):
        self._open_enrollment = new_open_enrollment

    def course_section_name(self):
        return f"{self.course.course_info()}/{self.section_number}"

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
