from __future__ import annotations

from src.Database.CourseMapper import CourseMapper
from src.Database.DatabaseHelper import DatabaseHelper
from src.Database.Mapper import Mapper


class CourseSectionMapper(Mapper):
    """
    singleton
    responsibility is to call the correct methods
    on database helper to get data required to build
    course sections

    because a course object is an integral part of
    the course section, creating a course object
    (via the course mapper) falls within this purview

    """

    def __init__(self):
        super().__init__()

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CourseSectionMapper.__instance == None:
            CourseSectionMapper()
        return CourseSectionMapper.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if CourseSectionMapper.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CourseSectionMapper.__instance = self

    def load(self, *, course_id: str, department: str, quarter: str, section_number: str) -> dict:
        """
        returns dict with data required for construction instead of
        object itself
        """
        db_helper = DatabaseHelper.getInstance()

        course_section_data = db_helper.load_course_section_by_id(
            course_id=course_id, department=department,
            quarter=quarter, section_number=section_number)
        course = self.__build_course(
            course_id=course_id, department=department)
        course_section_data['course'] = course
        return course_section_data

    def get_enrollment_total(self, *, course_id: str, department: str, quarter: str, section_number) -> int:
        db_helper = DatabaseHelper.getInstance()
        return db_helper.load_enrollment_total_for_course_section(
            course_id=course_id, department=department,
            quarter=quarter, section_number=section_number)

    def __build_course(self, course_id: str, department: str) -> Course:
        mapper = CourseMapper.getInstance()
        course = mapper.load(course_id=course_id, department=department)
        return course
