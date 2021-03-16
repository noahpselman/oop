class Singleton():
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance

    def __init__(self, decorated):
        """ Virtually private constructor. """
        # self.table_name = "log-message"
        if Singleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = decorated


if __name__ == "__main__":

    @Singleton
    class A():
        def __init__(self):
            self.data = {"some_data": 6}

        def a_method(self, arg):
            return arg ** 2

    a = A.getInstance()
    print(a)
    b = A.getInstance()
    print(b)
