from src.Database.CourseSectionMapper import CourseSectionMapper
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

    def build_course_sections(self, data):
        """
        data is list of dicts in which key-val pairs correspond to
        kwargs in build course section
        """
        print("data", data)
        return [self.build_course_section(**row) for row in data]

    def build_course_section(self, **kwargs):
        """
        kwargs must include:
            department: str
            course_id: str
            quarter: str
            section_number: str
        """
        print("build course section called in course seciton factory")
        course_section_mappper = CourseSectionMapper.getInstance()
        course_section = course_section_mappper.load(**kwargs)
        return course_section

        # course = self.__build_course(
        #     course_id=kwargs['course_id'], department=kwargs['department'])
        # kwargs['course'] = course
        # print(course)

        # timeslot = TimeSlot()
        # course_section = CourseSection(kwargs)
        # mapper = CourseSectionMapper.getIn

    # def __build_course(self, course_id: str, department: str):
    #     mapper = CourseMapper.getInstance()
    #     course = mapper.load(course_id=course_id, department=department)
    #     return course
