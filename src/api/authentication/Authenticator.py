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

    def authenticate_user(self, username: str, password: str):
        """
        obviously this is just a placeholder login
        """
        return True