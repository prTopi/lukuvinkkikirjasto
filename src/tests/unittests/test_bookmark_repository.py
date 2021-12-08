import unittest
from repositories.bookmark_repository import BookmarkRepository
from db import db

bookmark_repository = BookmarkRepository(db)


class TestBookmarkRepository(unittest.TestCase):
    def test_insert_bookmark_works(self):
        added_bookmarks = bookmark_repository.count_bookmarks()
        bookmark_id = bookmark_repository.insert_bookmark(1, "Description")
        bookmark = bookmark_repository.get_bookmark(bookmark_id)

        self.assertEqual(bookmark["bookmark_id"], added_bookmarks+1)
        self.assertEqual(bookmark["user_id"], 1)
        self.assertEqual(bookmark["description"], "Description")
        self.assertEqual(bookmark["unread"], False)
        self.assertIsNotNone(bookmark["date"])

    def test_insert_book_works(self):
        added_bookmarks = bookmark_repository.count_bookmarks()
        bookmark_id = bookmark_repository.insert_book(
            1, "Title of the book", "Description of the book", "Author", "978-951-98548-9-2")
        bookmark = bookmark_repository.get_book(bookmark_id)

        self.assertEqual(bookmark["bookmark_id"], added_bookmarks+1)
        self.assertEqual(bookmark["book_id"], 1)
        self.assertEqual(bookmark["user_id"], 1)
        self.assertEqual(bookmark["title"], "Title of the book")
        self.assertEqual(bookmark["description"], "Description of the book")
        self.assertEqual(bookmark["author"], "Author")
        self.assertEqual(bookmark["isbn"], "978-951-98548-9-2")
        self.assertEqual(bookmark["unread"], False)
        self.assertIsNotNone(bookmark["date"])

    def test_insert_video_works(self):
        added_bookmarks = bookmark_repository.count_bookmarks()
        bookmark_id = bookmark_repository.insert_video(
            1, "Title of the video", "Description of the video", "Creator", "https://youtu.be/dQw4w9WgXcQ")
        bookmark = bookmark_repository.get_video(bookmark_id)

        self.assertEqual(bookmark["bookmark_id"], added_bookmarks+1)
        self.assertEqual(bookmark["video_id"], 1)
        self.assertEqual(bookmark["user_id"], 1)
        self.assertEqual(bookmark["title"], "Title of the video")
        self.assertEqual(bookmark["description"], "Description of the video")
        self.assertEqual(bookmark["creator"], "Creator")
        self.assertEqual(bookmark["link"], "https://youtu.be/dQw4w9WgXcQ")
        self.assertEqual(bookmark["unread"], False)
        self.assertIsNotNone(bookmark["date"])

    def test_insert_blog_works(self):
        added_bookmarks = bookmark_repository.count_bookmarks()
        bookmark_id = bookmark_repository.insert_blog(
            1, "Title of the blog", "Description of the blog", "Creator", "https://www.lipsum.com/feed/html")
        bookmark = bookmark_repository.get_blog(bookmark_id)

        self.assertEqual(bookmark["bookmark_id"], added_bookmarks+1)
        self.assertEqual(bookmark["blog_id"], 1)
        self.assertEqual(bookmark["user_id"], 1)
        self.assertEqual(bookmark["title"], "Title of the blog")
        self.assertEqual(bookmark["description"], "Description of the blog")
        self.assertEqual(bookmark["creator"], "Creator")
        self.assertEqual(bookmark["link"], "https://www.lipsum.com/feed/html")
        self.assertEqual(bookmark["unread"], False)
        self.assertIsNotNone(bookmark["date"])

    def test_insert_podcast_works(self):
        added_bookmarks = bookmark_repository.count_bookmarks()
        bookmark_id = bookmark_repository.insert_podcast(
            1, "Name of the episode", "Name of the podcast",  "Description of the podcast", "Creator", "https://open.spotify.com/episode/6ZUtfzUjXc1xrkqChhfsTs?si=ff3f9b37994e41c5")
        bookmark = bookmark_repository.get_podcast(bookmark_id)

        self.assertEqual(bookmark["bookmark_id"], added_bookmarks+1)
        self.assertEqual(bookmark["podcast_id"], 1)
        self.assertEqual(bookmark["user_id"], 1)
        self.assertEqual(bookmark["episode_name"], "Name of the episode")
        self.assertEqual(bookmark["podcast_name"], "Name of the podcast")
        self.assertEqual(bookmark["description"], "Description of the podcast")
        self.assertEqual(bookmark["creator"], "Creator")
        self.assertEqual(
            bookmark["link"], "https://open.spotify.com/episode/6ZUtfzUjXc1xrkqChhfsTs?si=ff3f9b37994e41c5")
        self.assertEqual(bookmark["unread"], False)
        self.assertIsNotNone(bookmark["date"])

    def test_insert_scientific_article_works(self):
        added_bookmarks = bookmark_repository.count_bookmarks()
        bookmark_id = bookmark_repository.insert_scientific_article(
            1, "Title of the article", "Publication where article is", "Description of the article", "Authors", "10.1145/3293881.3295783", 2018, "Publisher of the article")
        bookmark = bookmark_repository.get_scientific_article(bookmark_id)

        self.assertEqual(bookmark["bookmark_id"], added_bookmarks+1)
        self.assertEqual(bookmark["scientific_article_id"], 1)
        self.assertEqual(bookmark["user_id"], 1)
        self.assertEqual(bookmark["title"], "Title of the article")
        self.assertEqual(bookmark["publication_title"],
                         "Publication where article is")
        self.assertEqual(bookmark["description"], "Description of the article")
        self.assertEqual(bookmark["authors"], "Authors")
        self.assertEqual(bookmark["doi"], "10.1145/3293881.3295783")
        self.assertEqual(bookmark["year"], 2018)
        self.assertEqual(bookmark["publisher"], "Publisher of the article")
        self.assertEqual(bookmark["unread"], False)
        self.assertIsNotNone(bookmark["date"])
    
    def test_add_new_tag(self):
        db.add_new_tag(1,"NewTag")
        users_tags = db.get_all_user_tags(1)
        added_tag = users_tags[0]

        self.assertEqual(len(users_tags),1)
        self.assertEqual(added_tag["user_id"],1)
        self.assertEqual(added_tag["tag_name"],"NewTag")

    def test_mark_tag_to_bookmark(self):
        db.mark_tag_to_bookmark(1,1,1)
        marked_tags = db.get_all_users_marked_tags(1)
        new_marked_tag = marked_tags[0]

        self.assertEqual(len(marked_tags),1)
        self.assertEqual(new_marked_tag["tag_id"],1)
        self.assertEqual(new_marked_tag["user_id"],1)
        self.assertEqual(new_marked_tag["bookmark_id"],1)