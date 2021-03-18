from abc import ABC, abstractmethod

from src.Database.DatabaseHelper import DatabaseHelper


class Mapper(ABC):

    def __init__(self):
        self.db_helper = DatabaseHelper.getInstance()

    @abstractmethod
    def load(self):
        pass
