from src.Database.CourseMapper import CourseMapper
from src.Entities.CourseSection import CourseSection
from src.Database.DatabaseHelper import DatabaseHelper
from src.Database.Mapper import Mapper


class CourseSectionMapper(Mapper):
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

    def load(self, **kwargs):
        """
        kwargs must include:
            course_id (str)
            department (str)

        """
        db_helper = DatabaseHelper.getInstance()
        course_section_data = db_helper.load_course_section_by_id(**kwargs)
        print("course section mapper printing data from database")
        course = self.__build_course(
            course_id=kwargs['course_id'], department=kwargs['department'])
        course_section_kwargs = {
            'section_number': course_section_data['section_number'],
            'enrollment_open': course_section_data['enrollment_open'],
            'capacity': course_section_data['capacity'],
            'quarter': course_section_data['quarter'],
            'course': course,
            'data': {
                'timeslot_id': course_section_data['timeslot'],
                'instructor_id': course_section_data['instructor_id']
            }
        }
        course_section = CourseSection(**course_section_kwargs)
        return course_section

    def __build_course(self, course_id: str, department: str):
        mapper = CourseMapper.getInstance()
        course = mapper.load(course_id=course_id, department=department)
        return course

    def save(self):
        pass
