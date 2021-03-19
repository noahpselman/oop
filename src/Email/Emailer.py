from __future__ import annotations
from src.Email.Engine import Engine


class Emailer():
    """
    silly little class that acts like it will send an
    email using an engine but in reality just prints
    a message
    """
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Emailer.__instance == None:
            Emailer()
        return Emailer.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Emailer.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Emailer.__instance = self

        self._engine = Engine()
        self._system_email_address = None

    @property
    def system_email_address(self):
        return self._system_email_address

    @system_email_address.setter
    def system_email_address(self, new_system_email_address):
        self._system_email_address = new_system_email_address

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, new_engine):
        self._engine = new_engine

    def send(self, *, to: List[str], msg: str):
        return self.engine.send(
            to=to, from_=self.system_email_address, msg=msg)
