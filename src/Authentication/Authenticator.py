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
        print("authenticator getting user_id", user_id)
        try:
            user_data = db_helper.load_user_by_id(user_id)
        except Exception as e:
            print(e)
            print("user not found")
            return False
        else:
            # print('user_data', user_data)
            return user_data['university_id']
