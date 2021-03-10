from abc import ABC, abstractmethod

from src.Database.DatabaseHelper import DatabaseHelper


class PermissionObjectFactory(ABC):

    @abstractmethod
    def save():
        pass

    @abstractmethod
    def build_email():
        pass

    @abstractmethod
    def build_notification():
        pass


class InstructorPermission(PermissionObjectFactory):

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if InstructorPermission.__instance == None:
            InstructorPermission()
        return InstructorPermission.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if InstructorPermission.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            InstructorPermission.__instance = self

    # def save(self,):
    #     db_helper = DatabaseHelper.getInstance()
