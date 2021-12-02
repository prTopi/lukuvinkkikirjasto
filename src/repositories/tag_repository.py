"""Module containing tag function"""

from db import add_new_tag, mark_tag_to_bookmark,get_all_user_tags,get_all_users_marked_tags

class TagRepository:
    """Tag repository to handle tags
    """
    def __init__(self,user_id):
        self.user_id = user_id

    def create_new_tag(self,tag_name):

        add_new_tag(self.user_id,tag_name)

    def mark_tag_to_bookmark(self,tag_id,bookmark_id):

        mark_tag_to_bookmark(tag_id,self.user_id,bookmark_id)

    def get_user_tags(self):
        return get_all_user_tags(self.user_id)

    def get_all_users_marked_tags(self):
        return get_all_users_marked_tags(self.user_id)
