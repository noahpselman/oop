from src.Database.Database import Database
import psycopg2 as pg
from psycopg2.extras import DictCursor
from src.db_conf import db_conf
from src.Entities.Quarter import Quarter
from src.Database.DatabaseHelper import DatabaseHelper
from src.Factories.UserEntityFactory import UserEntityFactory
from src.Authentication.Authenticator import Authenticator


class MainController():
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

        # self.CURRENT_QUARTER = self.get_current_quarter()

    # def get_current_quarter(self):
    #     today = datetime.date(datetime.now())
    #     db_helper = DatabaseHelper.getInstance()
    #     quarter_data = db_helper.get_current_quarter(today)
    #     return Quarter(**quarter_data)

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
        auth = Authenticator.getInstance()
        result = auth.authenticate_user(user_id, password)
        return result

    def setup_user(self, user_id):
        user_entity_factory = UserEntityFactory.getInstance()
        print("user id from setup_user", user_id)
        entity = user_entity_factory.build_from_id(user_id)
        print('entity from setup_user in main controller', entity)
        return entity

    def create_user(self, user_id: str):
        return User(user_id)

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
