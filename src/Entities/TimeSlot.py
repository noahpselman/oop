from __future__ import annotations
from datetime import datetime


class TimeSlot():

    def __init__(self, **kwargs) -> None:
        self.start_time: time = kwargs['start_time']
        self.end_time: time = kwargs['end_time']
        self.days: List[str] = kwargs['days']

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def days(self):
        return self._days

    def no_overlap(self, other_time_slot: TimeSlot):
        """
        returns true if time slots do not overlap
        """
        overlapping_days = []
        for d in self.days:
            for other_d in other_time_slot.days:
                if d == other_d:
                    overlapping_days.append(
                        (self.end_time < other_time_slot.start_time) or (
                            self.start_time > other_time_slot.end_time))
        return all(overlapping_days)

    def __repr__(self):
        return f"TimeSlot {self.days} {self.start_time}-{self.end_time}"

    def jsonify(self):
        return self.__dict__
