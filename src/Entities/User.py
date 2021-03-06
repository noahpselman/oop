

from src.Database.UserMapper import UserMapper


class User():

    def __init__(self, user_id: str) -> None:

        self._mapper = UserMapper(self)
        self._id: str = user_id

        self._full_name: str = None
        self._email: str = None
        self._user_type: str = None

        self._load()

    @property
    def mapper(self):
        return self._mapper

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, new_name: str):
        self._full_name = new_name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        self._email = new_email

    @property
    def id(self):
        return self._id

    @property
    def user_type(self):
        return self._user_type

    @user_type.setter
    def user_type(self, new_user_type):
        self._user_type = new_user_type

    def _load(self):
        self.mapper.load()

    def jsonify(self):
        result = {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "user_type": self.user_type
        }
        return result

    def __repr__(self):
        return f"""
        User Object
        {self.id}
        {self.full_name}
        {self.email}
        {self.user_type}
        """

    # def __downcast(self):
    #     """
    #     should only be called by UserController
    #     """
    #     return self.USER_TYPES[self.user_type](self)
