import unittest
from repositories.tag_repository import TagRepository
from db import db

tag_repository = TagRepository(db)


class TestBookmarkRepository(unittest.TestCase):
    def test_add_new_tag(self):
        tag_repository.create_new_tag(1, "NewTag")
        users_tags = tag_repository.get_user_tags(1)
        added_tag = users_tags[0]

        self.assertEqual(len(users_tags), 1)
        self.assertEqual(added_tag["user_id"], 1)
        self.assertEqual(added_tag["tag_name"], "NewTag")

    def test_mark_tag_to_bookmark(self):
        tag_repository.mark_tag_to_bookmark(1, 1, 1)
        marked_tags = tag_repository.get_all_users_marked_tags(1)
        new_marked_tag = marked_tags[0]

        self.assertEqual(len(marked_tags), 1)
        self.assertEqual(new_marked_tag["tag_id"], 1)
        self.assertEqual(new_marked_tag["user_id"], 1)
        self.assertEqual(new_marked_tag["bookmark_id"], 1)
