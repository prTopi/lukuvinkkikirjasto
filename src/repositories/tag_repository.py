"""Module containing tag function"""


class TagRepository:
    """Tag repository to handle tags
    """

    def __init__(self, db):
        self.db = db

    def create_new_tag(self, user_id, tag_name):
        sql = """
        INSERT INTO Tags
        (user_id, tag_name)
        VALUES
        (:user_id,:tag_name)
        """
        values = {
            "user_id": user_id,
            "tag_name": tag_name
        }
        self.db.session.execute(sql, values)
        self.db.session.commit()

    def mark_tag_to_bookmark(self, user_id, tag_id, bookmark_id):
        sql = """
        INSERT INTO Bookmarks_tags
        (tag_id, user_id, bookmark_id)
        VALUES
        (:tag_id, :user_id, :bookmark_id)
        """
        values = {
            "tag_id": tag_id,
            "user_id": user_id,
            "bookmark_id": bookmark_id
        }
        self.db.session.execute(sql, values)
        self.db.session.commit()

    def get_user_tags(self, user_id):
        sql = """
        SELECT id, user_id, tag_name
        FROM Tags
        WHERE user_id =:user_id
        """
        values = {
            "user_id": user_id
        }
        tags = self.db.session.execute(sql, values).fetchall()
        return tags

    def get_all_users_marked_tags(self, user_id):
        sql = """
        SELECT BT.tag_id, BT.user_id, BT.bookmark_id, T.tag_name
        FROM Bookmarks_tags BT
        JOIN Tags T ON T.id = BT.tag_id
        WHERE BT.user_id=:user_id

        """
        values = {
            "user_id": user_id
        }
        marked_tags = self.db.session.execute(sql, values).fetchall()
        return marked_tags
