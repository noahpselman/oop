from src.Database.Mapper import Mapper
from src.Database.DatabaseHelper import DatabaseHelper


class UserMapper(Mapper):

    def __init__(self, user):
        super().__init__()
        self.user = user

    def load(self):
        try:
            loaded_data = self.db_helper.load_user_by_id(self.user.id)
            print("loaded data:", loaded_data)
            self.user.full_name = loaded_data['name']
            self.user.email = loaded_data['email']
            self.user.user_type = loaded_data['user_type']
            return self.user
        except Exception as e:
            print(e)
            return False

    def save():
        pass
