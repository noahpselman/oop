from __future__ import annotations

from src.Entities.User import User
from src.Database.InstructorMapper import InstructorMapper
from src.Database.StudentMapper import StudentMapper


class UserEntityFactory():
    """
    Builds specific entities representing users from User object
    """

    USER_MAPPERS = {
        "Student": StudentMapper,
        "Instructor": InstructorMapper
    }

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if UserEntityFactory.__instance == None:
            UserEntityFactory()
        return UserEntityFactory.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if UserEntityFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            UserEntityFactory.__instance = self

    def __build_user(self, user_id: str):
        return User(user_id)

    def build_from_id(self, user_id: str) -> ControlleeInterface:

        user = self.__build_user(user_id)
        mapper = self.USER_MAPPERS[user.user_type].getInstance()
        entity = mapper.load(user)

        return entity

        # Mapper = self.USER_MAPPERS[user.type]
        # mapper = Mapper()
        # entity = mapper.load(user)
        # return entity
