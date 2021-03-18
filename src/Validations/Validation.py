from __future__ import annotations
from abc import ABC, abstractmethod


class Validation(ABC):

    @abstractmethod
    def is_valid(self, student: Student, course_section: CourseSection):
        pass
