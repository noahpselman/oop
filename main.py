"""
script for testing without using api
"""
from src.Controllers.MainController import MainController
from src.Constants.Restrictions import LibraryRestriction
from src.Factories.UserEntityFactory import UserEntityFactory
import psycopg2 as pg
from psycopg2.extras import DictCursor
import json

from src.db_conf import db_conf
from src.Database.Database import Database
from src.Database.DatabaseHelper import DatabaseHelper

if __name__ == "__main__":
    db_config = db_conf()

    print(db_config)

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
    db_helper = DatabaseHelper.getInstance()

    print("db_helper:", db_helper)

    # uef = UserEntityFactory.getInstance()
    # student = uef.build_from_id('89')
    # print("past courses", student.course_history)

    from src.util import get_past_quarters
    get_past_quarters()

    # controller = MainController.getInstance()
    # print(controller.CURRENT_QUARTER)
    # student.restrictions = [LibraryRestriction]
    # print(student.user_data.jsonify())
