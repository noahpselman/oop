from src.Controllers.RegistrationFailureManager import RegistrationFailureManager
from src.Controllers.RequestManager import RequestManager
from src.Controllers.SearchManager import SearchManager
from src.util import parse_section_index
from src.Factories.UserEntityFactory import UserEntityFactory
from src.Authentication.Authenticator import Authenticator
from src.Factories.CourseSectionFactory import CourseSectionFactory
from src.Controllers.Registrar import Registrar


class MainController():
    """
    responsible for taking data from the router and
    calling appropriate application methods
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if MainController.__instance == None:
            MainController()
        return MainController.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if MainController.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            MainController.__instance = self

    def login(self, user_id, password):
        print("controller getting user_id", user_id)

        auth = Authenticator.getInstance()
        result = auth.authenticate_user(user_id, password)
        return result

    def __setup_user(self, user_id):
        user_entity_factory = UserEntityFactory.getInstance()
        entity = user_entity_factory.build_from_id(user_id)
        return entity

    def __setup_course_section(self, *,
                               section_number: str, course_id: str,
                               department: str, quarter: str):
        """
        course_section_data must include:

        """
        course_section_factory = CourseSectionFactory.getInstance()
        course_section = course_section_factory.build_course_section(
            section_number=section_number, course_id=course_id,
            department=department, quarter=quarter)
        return course_section

    def request_permission(self, *, permission_type: str, student_id: str, section_index: str):
        student = self.__setup_user(student_id)
        course_section_data = parse_section_index(section_index)
        course_section = self.__setup_course_section(**course_section_data)
        request_manager = RequestManager.getInstance()
        result = request_manager.request_permission(
            student=student, course_section=course_section, permission_type=permission_type)

        return result

    def register(self, *, student_id: str, section_index: str):
        section_ids = parse_section_index(section_index)
        course_section = self.__setup_course_section(**section_ids)
        student = self.__setup_user(student_id)
        registrar = Registrar.getInstance()
        report = registrar.register_for_course(
            student=student, course_section=course_section)

        # some validation failures require returning search results
        fail_manager = RegistrationFailureManager()
        results = fail_manager.execute(
            course_section=course_section, report=report)

        return {
            'report': report,
            'student': student,
            'search_results': results['search_results'],
            'search_type': results['search_type']
        }

    def register_for_lab(self, *,
                         student_id: str, section_index: str, lab_index: str):
        section_ids = parse_section_index(section_index)
        course_section = self.__setup_course_section(**section_ids)
        lab_ids = parse_section_index(lab_index)
        lab_section = self.__setup_course_section(**lab_ids)
        student = self.__setup_user(student_id)
        registrar = Registrar.getInstance()
        report = registrar.register_for_lab(
            student=student, course_section=course_section, lab_section=lab_section)

        fail_manager = RegistrationFailureManager()
        results = fail_manager.execute(
            course_section=course_section, report=report)

        return {
            'report': report,
            'student': student,
            'search_results': results['search_results'],
            'search_type': results['search_type']
        }

    def drop_course(self, *, student_id: str, section_index: str):

        section_ids = parse_section_index(section_index)
        course_section = self.__setup_course_section(**section_ids)
        student = self.__setup_user(student_id)
        registrar = Registrar.getInstance()
        report = registrar.drop_course(student, course_section)
        return {'report': report, 'student': student}

    def search_for_course_section(self, search_dict):
        """
        search_dict has atleast one of the keys:
            'department': str
            'course_number'str
            'instructor'str
        """
        print("searching with the following criteria")
        print("search dict")
        search_manager = SearchManager.getInstance()
        result = search_manager.execute(search_dict)
        return result

    def get_current_courses(self, *, student_id: str, quarter: str):
        student = self.__setup_user(student_id)
        result = student.get_courses_by_quarter(quarter)
        return {'student': student, 'courses': result}
