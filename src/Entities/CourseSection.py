from __future__ import annotations
from src.util import get_current_quarter


class CourseSection():
    pass
    # def __init__(self) -> None:

    def __init__(self, **kwargs) -> None:

        self.section_number: str = kwargs['section_number']
        self._course: str = kwargs['course']
        self._timeslot: Timeslot = kwargs['timeslot']
        self._lead_instructor: Instructor = kwargs['lead_instructor']
        self._enrollment_open: bool = kwargs['enrollment_open']

    @property
    def section_number(self):
        return self._section_number

    @property
    def quarter(self):
        return self._quarter

    @property
    def timeslot(self):
        return self._timeslot

    @property
    def open_enrollment(self):
        return self._open_enrollment

    @open_enrollment.setter
    def open_enrollment(self, new_open_enrollment):
        self._open_enrollment = new_open_enrollment
