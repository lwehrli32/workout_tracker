from flask_login import current_user
class user_manager():

    def __init__(self):
        pass

    def add_user(self):
        return None

    def get_user_id(self):
        return current_user.id
