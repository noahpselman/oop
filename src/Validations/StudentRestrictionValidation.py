from __future__ import annotations
from src.Validations.Validation import Validation


class StudentRestrictionValidation(Validation):

    __instance = None

    @ staticmethod
    def getInstance():
        """ Static access method. """
        if StudentRestrictionValidation.__instance == None:
            StudentRestrictionValidation()
        return StudentRestrictionValidation.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self._conn = None
        if StudentRestrictionValidation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            StudentRestrictionValidation.__instance = self

    def is_valid(self, report, **kwargs):
        print("student restriction validator doing its thang")
        student = kwargs['student']
        restrictions = student.restrictions

        validation = self.__class__.__name__
        success = not restrictions
        msg = self.__write_msg(restrictions)
        report.add_data(validation=validation, success=success, msg=msg)

    def __write_msg(self, restrictions):
        print("restrictions", restrictions)
        if not restrictions:
            return "You have no restrictions"
        else:
            return "You have the following restrictions on your account: " + \
                ', '.join(restrictions)
