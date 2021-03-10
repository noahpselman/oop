from src.Database.DatabaseHelper import DatabaseHelper


class Authenticator():
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Authenticator.__instance == None:
            Authenticator()
        return Authenticator.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Authenticator.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Authenticator.__instance = self

    def authenticate_user(self, user_id: str, password: str):
        """
        obviously this is just a placeholder login
        """
        db_helper = DatabaseHelper.getInstance()
        try:
            user_data = db_helper.load_user_by_id(user_id)
        except:
            print("user not found")
            return False
        else:
            return user_data['university_id']
