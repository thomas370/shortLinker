from flask_login import UserMixin
from utils.db import cursor


class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @staticmethod
    def get(user_id):
        """
        Récupère un utilisateur depuis la DB à partir de son ID
        (obligatoire pour flask-login)
        """
        cursor.execute(
            "SELECT id, username FROM users WHERE id = %s",
            (user_id,)
        )
        user = cursor.fetchone()
        if user:
            return User(user["id"], user["username"])
        return None
