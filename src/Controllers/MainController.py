from src.Controllers.RequestManager import RequestManager
from src.Controllers.SearchManager import SearchManager
from src.util import parse_section_index
from src.Database.Database import Database
import psycopg2 as pg
from psycopg2.extras import DictCursor, register_composite
from src.db_conf import db_conf
from src.Entities.Quarter import Quarter
from src.Database.DatabaseHelper import DatabaseHelper
from src.Factories.UserEntityFactory import UserEntityFactory
from src.Authentication.Authenticator import Authenticator
from src.Factories.CourseSectionFactory import CourseSectionFactory
from src.Controllers.Registrar import Registrar
from src.Logging.Logger import Logger


class MainController():
    __instance = None
    logger = Logger.getInstance()

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

    def setup_db(self):
        db_config = db_conf()

        try:
            connection = pg.connect(
                dbname=db_config['dbname'],
                user=db_config['user'],
                password=db_config['password'],
                host=db_config['host'],
                port=db_config['port'],
                cursor_factory=DictCursor
            )
        except KeyError as e:
            print("Unable to connect to the databse with db_config")
            raise

        print("connection:", connection)
        db = Database.getInstance()
        db.conn = connection

    def login(self, user_id, password):
        self.logger.log(context=self.__class__.__name__, method="login",
                        msg=f"login called with args {user_id}, {password}")
        print("controller getting user_id", user_id)

        auth = Authenticator.getInstance()
        result = auth.authenticate_user(user_id, password)
        return result

    def setup_user(self, user_id):
        user_entity_factory = UserEntityFactory.getInstance()
        print("user id from setup_user", user_id)
        entity = user_entity_factory.build_from_id(user_id)
        print('entity from setup_user in main controller', entity)
        return entity

    # using * in the parameters is a lesser known technique for making
    # the following parameters required keyword arguments
    def setup_course_section(self, *,
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

    # def request_instr_permission(self, *, student_id: str,
    #                              section_number: str, course_id: str,
    #                              department: str, quarter: str):
    #     student = self.setup_user_entity('student_id')
    #     course_section = self.setup_course_section('course_section')
    #     factory = RequestFactory.getInstance()
    #     factory.build('instructor_permission')
    #     request_manager = RequestManager.getInstance()
    #     request_manager.execute

        # send email
        # input into db
        # return result

    def register(self, *, student_id: str, section_index: str):
        section_ids = parse_section_index(section_index)
        course_section = self.setup_course_section(**section_ids)
        student = self.setup_user(student_id)
        registrar = Registrar.getInstance()
        report = registrar.register_for_course(student, course_section)
        # i know i shouldn't have the main controller knowing the
        # structure of the report but i have to do something special
        # if there's a corresponding lab
        print(report)
        if not report['details']['LabValidation']['success']:
            result = self.search_for_course_section({
                'quarter': course_section.quarter,
                'course_id': course_section.lab.course_id})
            report['search_results'] = result

        return {'report': report, 'student': student}

    def drop_course(self, *, student_id: str, section_index: str):

        section_ids = parse_section_index(section_index)
        course_section = self.setup_course_section(**section_ids)
        student = self.setup_user(student_id)
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

    # def create_user(self, user_id: str):
    #     return User(user_id)

    # def create_user_entity(self, user: User):
    #     if user.user_type == "Student":
    #         f = StudentFactory(user)
    #     elif user.user_type == "Instructor":
    #         f = InstructorFactory(user)

    # def create_controller(self, user: User):
    #     """
    #     Maybe this could be brought outside somewhere
    #     """
    #     if user.user_type == "Student":
    #         cf = StudentControllerFactory()
    #     elif user.user_type == "Instructor":
    #         cf = InstructorControllerFactory()

    #     return cf.execute_build(user)

    # def create_user_entity(self, user: User):
    #     Mapper = MainController.USER_CLASSES[user.user_type]['mapper']
    #     mapper = Mapper()
    #     return mapper.load(user=user)

    # def create_user_controller(self, user_entity):
    #     Controller = MainController.USER_CLASSES[user_entity.user_data.user_type]['controller']
    #     controller = Controller()
    #     controller.user_entity = user_entity
    #     return controller
