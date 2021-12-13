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
        self.assertEqual(bookmark["book_id"], 2)
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
        self.assertEqual(bookmark["video_id"], 2)
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
        self.assertEqual(bookmark["blog_id"], 2)
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
        self.assertEqual(bookmark["podcast_id"], 2)
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
        self.assertEqual(bookmark["scientific_article_id"], 2)
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

    def test_edit_book(self):
        bookmark_id = bookmark_repository.insert_book(
            1, "Title", "Description", "Author", "978-951-98548-9-2")
        book = bookmark_repository.get_book(bookmark_id)
        bookmark_repository.edit_book(book["book_id"],bookmark_id, "new title", "New Author", "978-3-16-148410-0", "Description of book", True)
        updated_book = bookmark_repository.get_book(bookmark_id)
        self.assertEqual(updated_book["title"], "new title")
        self.assertEqual(updated_book["author"], "New Author")
        self.assertEqual(updated_book["isbn"], "978-3-16-148410-0")
        self.assertEqual(updated_book["description"], "Description of book")
        self.assertEqual(updated_book["unread"], True)
    
    def test_edit_video(self):
        bookmark_id = bookmark_repository.insert_video(
            1, "Title of the video", "Description of the video", "Creator", "https://youtu.be/dQw4w9WgXcQ")
        video = bookmark_repository.get_video(bookmark_id)
        bookmark_repository.edit_video(video["video_id"],video["bookmark_id"], "New title", "I", "https://youtube.com", "New Description", True)
        updated_video = bookmark_repository.get_video(bookmark_id)
        self.assertEqual(updated_video["title"], "New title")
        self.assertEqual(updated_video["creator"], "I")
        self.assertEqual(updated_video["link"], "https://youtube.com")
        self.assertEqual(updated_video["unread"], True)
        self.assertEqual(updated_video["description"], "New Description")
    
    def test_edit_blog(self):
        bookmark_id = bookmark_repository.insert_blog(
            1, "Title of the blog", "Description of the blog", "Creator", "https://www.lipsum.com/feed/html")
        blog = bookmark_repository.get_blog(bookmark_id)
        bookmark_repository.edit_blog(blog["blog_id"],blog["bookmark_id"], "New title", "New creator", "https://www.lipsum.com/","Updated description",True)
        updated_blog = bookmark_repository.get_blog(bookmark_id)
        self.assertEqual(updated_blog["title"], "New title")
        self.assertEqual(updated_blog["creator"], "New creator")
        self.assertEqual(updated_blog["link"], "https://www.lipsum.com/")
        self.assertEqual(updated_blog["unread"], True)
        self.assertEqual(updated_blog["description"], "Updated description")
    
    def test_edit_podcast(self):
        bookmark_id = bookmark_repository.insert_podcast(
            1, "Name of the episode", "Name of the podcast",  "Description of the podcast", "Creator", "https://open.spotify.com/episode/6ZUtfzUjXc1xrkqChhfsTs?si=ff3f9b37994e41c5")
        podcast = bookmark_repository.get_podcast(bookmark_id)
        bookmark_repository.edit_podcast(podcast["podcast_id"],podcast["bookmark_id"], "new podcast name", "New Creator", "episode 3.14", "https://open.spotify.com/episode/4yTlC6q1Seg39BCS7w23b6?si=3e56785251614e40", "Desctiption of the episode", True)
        updated_podcast = bookmark_repository.get_podcast(bookmark_id)
        self.assertEqual(updated_podcast["podcast_name"], "new podcast name")
        self.assertEqual(updated_podcast["creator"], "New Creator")
        self.assertEqual(updated_podcast["episode_name"], "episode 3.14")
        self.assertEqual(updated_podcast["link"],"https://open.spotify.com/episode/4yTlC6q1Seg39BCS7w23b6?si=3e56785251614e40")
        self.assertEqual(updated_podcast["unread"], True)
        self.assertEqual(updated_podcast["description"], "Desctiption of the episode")
    
    def test_edit_scientific_article(self):
        bookmark_id = bookmark_repository.insert_scientific_article(
            1, "Title of the article", "Publication where article is", "Description of the article", "Authors", "10.1145/3293881.3295783", 2018, "Publisher of the article")
        article = bookmark_repository.get_scientific_article(bookmark_id)
        bookmark_repository.edit_scientific_article(article["scientific_article_id"], article["bookmark_id"], "Title", "New authors", "pub title", "10.1145", 2021, "publisher","description",True)
        updated_article = bookmark_repository.get_scientific_article(bookmark_id)
        self.assertEqual(updated_article["title"], "Title")
        self.assertEqual(updated_article["publication_title"], "pub title")
        self.assertEqual(updated_article["description"], "description")
        self.assertEqual(updated_article["authors"], "New authors")
        self.assertEqual(updated_article["doi"], "10.1145")
        self.assertEqual(updated_article["publisher"], "publisher")
        self.assertEqual(updated_article["year"], 2021)
        self.assertEqual(updated_article["unread"], True)
