from __future__ import annotations

from src.Entities.User import User
from src.Database.InstructorMapper import InstructorMapper
from src.Database.StudentMapper import StudentMapper


class UserEntityFactory():
    """
    Builds specific entities representing users from User object

    I had an option to implement the factory method pattern here
    and have a student factory and instructor factory.  I chose not
    to because that didn't seem like it would require something
    upstream to know which factory to use.  This way the factory
    can figure what to output and everything outside doesn't have
    to worry about that - they just know they're going to get what
    they want by passing in a user id string - while this is not a
    design pattern I recognize it feels a lot cleaner and doesn't
    really violate the single responsibility principle
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
        print(user)
        mapper = self.USER_MAPPERS[user.user_type].getInstance()
        entity = mapper.load(user)

        return entity
