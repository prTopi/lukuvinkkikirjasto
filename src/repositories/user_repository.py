
"""Module containing tag function"""


class UserRepository:
    """Tag repository to handle tags
    """

    def __init__(self, db):
        self.db = db

    def find_user_id(self, username):
        sql = "SELECT id FROM Users WHERE username=:username"
        try:
            return self.db.session.execute(sql, {"username": username}).fetchone()[0]
        except (IndexError, TypeError):
            return None

    def find_password(self, username):
        sql = "SELECT password FROM Users WHERE username=:username"
        return self.db.session.execute(sql, {"username": username}).fetchone()

    def insert_user(self, username, password):
        sql = """
        INSERT INTO Users (username, password)
        VALUES (:username, :password)
        """
        self.db.session.execute(
            sql, {"username": username, "password": password})
        self.db.session.commit()
