from src.Database.CourseSectionMapper import CourseSectionMapper
from src.Entities.CourseSection import CourseSection


class CourseSectionFactory():
    """
    singleton
    responsibility is to create a single creation point
    for course section objects

    course section mapper will take care of the details of
    loading the data from the database (including composing
    objects) from db

    all the factory does is call the correct method on the
    mapper and piece the data together to deliver a
    course section object
    """

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

    def build_course_sections(self, course_section_data):
        """
        course_section_data is list of dicts in which key-val pairs correspond to
        kwargs in build course section
        """
        return [self.build_course_section(**row) for row in course_section_data]

    def build_course_section(self, *,
                             course_id: str, department: str, quarter: str,
                             section_number: str, **kwargs):
        """
        kwargs are here to allow other objects to use this method without
        knowing the specific arguments - instead they can just toss
        whatever comes back from the database
        """
        course_section_mappper = CourseSectionMapper.getInstance()
        course_section_data = course_section_mappper.load(
            course_id=course_id, section_number=section_number,
            department=department, quarter=quarter)

        # needs to be done because course_section_data contains
        # keys that are not parameters to course_section
        course_section_kwargs = {
            'section_number': course_section_data['section_number'],
            'enrollment_open': course_section_data['enrollment_open'],
            'capacity': course_section_data['capacity'],
            'quarter': course_section_data['quarter'],
            'state': course_section_data['state'],
            'instructor_permission_required': course_section_data['instructor_permission_required'],
            'course': course_section_data['course'],
            'data': {
                'timeslot_id': course_section_data['timeslot'],
                'instructor_id': course_section_data['instructor_id']
            }
        }

        course_section = CourseSection(**course_section_kwargs)

        return course_section
