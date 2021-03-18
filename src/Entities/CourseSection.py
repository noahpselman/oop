from __future__ import annotations

from src.Database.TimeSlotMapper import TimeSlotMapper
from src.Entities.TimeSlot import TimeSlot
from src.util import get_current_quarter, make_section_index


class CourseSection():
    """
    responsible for holding data relavant to individual course
    sections and responding to messages from those involved
    with registration process

    the instructor and timeslot attributes can be lazily loaded
    using the loading_data attribute - while it makes sense
    for the course section to know how to load itself, this could
    be refactored such that this information is loaded from 
    just the section_number, department, quarter, and course_id

    state can take 3 values: PRESTART, ONGOING, FINISHED

    jsonify method turns it into a json object that can 
    be sent to the front end
    """

    def __init__(self, *,
                 section_number: str,
                 enrollment_open: bool,
                 course: Course,
                 quarter: str,
                 data: dict,
                 capacity: int,
                 state: str,
                 instructor_permission_required: bool) -> None:
        """
        # TODO
        data is a dictionary that includes data required to
        lazily load instructor (instructor_id) and timeslot(timeslot_id)

        these could be refactored so that they can be loaded by id data
        (section_number, department, quarter, course_id)
        this is a lower priority to-do item
        """

        self._section_number = section_number
        self._enrollment_open = enrollment_open
        self._course = course
        self._quarter = quarter
        self._loading_data = data
        self._capacity = capacity
        self._state = state
        self._instructor_permission_required = instructor_permission_required

        # instantiating the roster is out of scope of this prototype
        self._roster: List[str] = []

    @property
    def lab(self):
        return self._course.lab

    @property
    def instructor_email(self):
        return self.instructor.email

    @property
    def course_info(self):
        """
        displays string of the non-section specific course
        identification info
        """
        return self._course.course_info

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
        return self._course.course_id

    @property
    def department(self):
        return self._course.department

    @property
    def capacity(self):
        return self._capacity

    @property
    def instructor(self):
        # importing here to avoid circular import error
        from src.Factories.UserEntityFactory import UserEntityFactory
        factory = UserEntityFactory.getInstance()
        instructor = factory.build_from_id(
            self._loading_data['instructor_id'])
        return instructor

    @property
    def section_number(self):
        return self._section_number

    @property
    def quarter(self):
        return self._quarter

    @property
    def timeslot(self):
        return self.__load_timeslot()

    def __load_timeslot(self):
        mapper = TimeSlotMapper.getInstance()
        return mapper.load(self._loading_data['timeslot_id'])

    @property
    def enrollment_open(self):
        return self._enrollment_open

    @property
    def course_section_name(self):
        """
        returns a string representing section identification
        information in a human-intuitive form
        """
        kwargs = {
            'department': self.department,
            'course_id': self.course_id,
            'section_number': self.section_number,
            'quarter': self.quarter
        }
        return make_section_index(**kwargs)

    def __repr__(self):
        return self.course_section_name

    def jsonify(self):
        result = {
            'section_index': self.course_section_name,
            'section_number': self.section_number,
            'enrollment_open': self.enrollment_open,
            'course': self.course.jsonify(),
            'quarter': self.quarter,
            'capacity': self.capacity,
            'instructor': self.instructor.jsonify(),
            'timeslot': self.timeslot.jsonify(),
            'enrollment_count': self.get_enrollment_total(),
            'instructor_permission_required': self._instructor_permission_required
        }
        return result
