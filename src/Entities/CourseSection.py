from __future__ import annotations
from src.util import get_current_quarter


class CourseSection():
    pass
    # def __init__(self) -> None:

    def __init__(self, **kwargs) -> None:

        self._course = kwargs['course']
        self._timeslot = kwargs['timeslot']
        self._open_enrollment: bool = False

    @property
    def quarter(self):
        return self._quarter

    @property
    def timeslot(self):
        return self._timeslot

    @property
    def open_enrollment(self):
        return self._open_enrollment

    @quarter.setter
    def quarter(self, new_quarter):
        self._quarter = new_quarter

    @timeslot.setter
    def timeslot(self, new_timeslot):
        self._timeslot = new_timeslot

    @open_enrollment.setter
    def open_enrollment(self, new_open_enrollment):
        self._open_enrollment = new_open_enrollment
