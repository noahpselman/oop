from __future__ import annotations
from datetime import time
from typing import List


class TimeSlot():
    """
    holds information relevant for class time slots
    also has a super conveninent method for making
    sure two timeslots don't overlap
    """

    def __init__(self, *, start_time, end_time, days) -> None:
        """
        kwargs are just the things you see in this here constructor
        """
        self._start_time: time = start_time
        self._end_time: time = end_time
        self._days: List[str] = days

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
                        (self.end_time <= other_time_slot.start_time) or (
                            self.start_time >= other_time_slot.end_time))
        return all(overlapping_days)

    def __repr__(self):
        return f"TimeSlot {self.days} {self.start_time}-{self.end_time}"

    def jsonify(self):
        result = {
            'start_time': str(self.start_time),
            'end_time': str(self.end_time),
            'days': self.days
        }
        return result
