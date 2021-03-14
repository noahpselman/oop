from src.db_conf import mongo_conf
import pymongo
from pymongo import MongoClient

# cluster = MongoClient(
#     "mongodb+srv://oop-proj:best-proj-ever99@cluster0.bez9g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# db = cluster["oop-proj-logging"]
# collection = db["log-messages"]

# data = {"_id": "test", "value": "this is a test log message"}

# collection.insert_one(data)


class MongoDatabase():

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if MongoDatabase.__instance == None:
            MongoDatabase()
        return MongoDatabase.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if MongoDatabase.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            MongoDatabase.__instance = self
        key = mongo_conf()
        self.cluster = MongoClient(key)
        self.db = self.cluster["oop-proj-logging"]
        # self.collection = self.db["log-messages"]

    def create(self, collection_name: str, values: dict):
        """
        values has variable name as key and value as value
        """
        try:
            collection = self.db[collection_name]
            collection.insert_one(values)
            return True
        except Exception as e:
            print(e)
            return False
