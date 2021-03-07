from src.Database.CourseMapper import CourseMapper
from src.Entities.TimeSlot import TimeSlot
from src.Entities.CourseSection import CourseSection
from src.Entities.Course import Course
from src.Entities.CourseSectionWarehouse import CourseSectionWarehouse


class CourseSectionFactory():

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CourseSectionFactory.__instance == None:
            CourseSectionFactory()
        return CourseSectionFactory.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if CourseSectionFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CourseSectionFactory.__instance = self

        self.warehouse = CourseSectionWarehouse.getInstance()

    def build_course_section(self, **kwargs):
        """
        kwargs are the arguments to the constructor of a course section
        """
        print("build course section called in course seciton factory")

        course = self.__build_course(
            course_id=kwargs['course_id'], department=kwargs['department'])
        kwargs['course'] = course
        print(course)
        # timeslot = TimeSlot()
        # course_section = CourseSection(kwargs)
        # mapper = CourseSectionMapper.getIn

    def __build_course(self, course_id: str, department: str):
        mapper = CourseMapper.getInstance()
        course = mapper.load(course_id=course_id, department=department)
        return course
