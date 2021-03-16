import datetime
from src.Database.MongoDatabase import MongoDatabase


class Logger():
    __instance = None
    table_name = "log-messages"

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Logger.__instance == None:
            Logger()
        return Logger.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self.db = MongoDatabase.getInstance()
        # self.table_name = "log-message"
        if Logger.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Logger.__instance = self

    def log(self, *, context, method, msg, args=[]):
        post = {
            "class": context,
            "method": method,
            "msg": msg,
            "timestamp": datetime.datetime.utcnow()
        }
        if args:
            post['args'] = ', '.join(args)
        print("logger logging", post)
        return self.db.create(self.table_name, post)
