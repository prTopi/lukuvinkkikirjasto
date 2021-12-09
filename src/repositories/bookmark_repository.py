
"""Module containing tag function"""


class BookmarkRepository:
    """Tag repository to handle tags
    """

    def __init__(self, db):
        self.db = db

    def insert_bookmark(self, user_id: int, description: str) -> int:
        """insert_bookmark is used to add basic info of any type
        into the database

        Args:
            user_id (int): id of the bookmark's owner
            description (str): description of the bookmark

        Returns:
            int: id of created bookmark
        """
        sql = """
        INSERT INTO Bookmarks
        (user_id, description)
        VALUES (:user_id, :description)
        RETURNING id
        """
        values = {
            "user_id": user_id,
            "description": description
        }
        bookmark_id = self.db.session.execute(sql, values).fetchone()[0]
        return bookmark_id

    def get_bookmark(self, bookmark_id: int) -> dict:
        """get_bookmark returns bookmark related to given bookmark id

        Args:
            bookmark_id (int): id of the bookmark

        Returns:
            dict: bookmark
        """
        sql = """
        SELECT id, user_id, description, unread, date
        FROM Bookmarks
        WHERE id=:id
        """
        bookmark = self.db.session.execute(sql, {"id": bookmark_id}).fetchone()
        return {
            "bookmark_id": bookmark[0],
            "user_id": bookmark[1],
            "description": bookmark[2],
            "unread": bookmark[3],
            "date": bookmark[4]
        }

    def count_bookmarks(self) -> int:
        sql = """
        SELECT COUNT(id) FROM Bookmarks
        """
        count = self.db.session.execute(sql).fetchone()[0]
        return count

    def insert_book(self, user_id: int, title: str, description: str,
                    author: str, isbn: str) -> int:
        """insert_book is used to add bookmark, which is type of
        book into the database

        Args:
            user_id (int): id of the bookmark's owner
            title (str): title of the book
            description (str): description of the book
            author (str): author(s) of the book
            isbn (str): isbn code of the book

        Returns:
            int: id of the bookmark (references into bookmarks table)
        """
        bookmark_id = self.insert_bookmark(user_id, description)
        sql = """
        INSERT INTO Books
        (bookmark_id, title, author, ISBN)
        VALUES (:bookmark_id, :title, :author, :isbn)
        """
        values = {
            "bookmark_id": bookmark_id,
            "title": title,
            "author": author,
            "isbn": isbn
        }
        self.db.session.execute(sql, values)
        self.db.session.commit()
        return bookmark_id

    def get_book(self, bookmark_id: int) -> dict:
        """get_book returns book related to given bookmark id

        Args:
            bookmark_id (int): id of the bookmark

        Returns:
            dict: searched bookmark
        """
        sql = """
        SELECT BM.id, B.id, BM.user_id, B.title, BM.description, B.author, B.isbn, BM.unread, BM.date
        FROM Bookmarks BM
        JOIN Books B ON BM.id = B.bookmark_id
        WHERE BM.id=:id
        """
        bookmark = self.db.session.execute(sql, {"id": bookmark_id}).fetchone()
        return {
            "bookmark_id": bookmark[0],
            "book_id": bookmark[1],
            "user_id": bookmark[2],
            "title": bookmark[3],
            "description": bookmark[4],
            "author": bookmark[5],
            "isbn": bookmark[6],
            "unread": bookmark[7],
            "date": bookmark[8]
        }

    def insert_video(self, user_id: int, title: str, description: str,
                     creator: str, link: str) -> int:
        """insert_video is used to add bookmark, which is type of
        video into the database

        Args:
            user_id (int): id of the bookmark's owner
            title (str): title of the video
            description (str): description of the video
            creator (str): creator of the video
            link (str): url referencing into the video

        Returns:
            int: id of the bookmark (references into bookmarks table)
        """
        bookmark_id = self.insert_bookmark(user_id, description)
        sql = """
        INSERT INTO Videos
        (bookmark_id, title, creator, link)
        VALUES (:bookmark_id, :title, :creator, :link)
        """
        values = {
            "bookmark_id": bookmark_id,
            "title": title,
            "creator": creator,
            "link": link
        }
        self.db.session.execute(sql, values)
        self.db.session.commit()
        return bookmark_id

    def get_video(self, bookmark_id: int) -> dict:
        """get_video returns video related to given bookmark id

        Args:
            bookmark_id (int): id of the bookmark

        Returns:
            dict: searched bookmark
        """
        sql = """
        SELECT BM.id, V.id, BM.user_id, V.title, BM.description, V.creator, V.link, BM.unread, BM.date
        FROM Bookmarks BM
        JOIN Videos V ON BM.id = V.bookmark_id
        WHERE BM.id=:id
        """
        bookmark = self.db.session.execute(sql, {"id": bookmark_id}).fetchone()
        if bookmark is None:
            return None
        return {
            "bookmark_id": bookmark[0],
            "video_id": bookmark[1],
            "user_id": bookmark[2],
            "title": bookmark[3],
            "description": bookmark[4],
            "creator": bookmark[5],
            "link": bookmark[6],
            "unread": bookmark[7],
            "date": bookmark[8]
        }

    def insert_blog(self, user_id: int, title: str, description: str,
                    creator: str, link: str) -> int:
        """insert_blog is used to add bookmark, which is type of
        blog into the database

        Args:
            user_id (int): id of the bookmark's owner
            title (str): title of the blog
            description (str): description of the blog
            creator (str): creator of the blog
            link (str): url referencing into the blog

        Returns:
            int: id of the bookmark (references into bookmarks table)
        """
        bookmark_id = self.insert_bookmark(user_id, description)
        sql = """
        INSERT INTO Blogs
        (bookmark_id, title, creator, link)
        VALUES (:bookmark_id, :title, :creator, :link)
        """
        values = {
            "bookmark_id": bookmark_id,
            "title": title,
            "creator": creator,
            "link": link
        }
        self.db.session.execute(sql, values)
        self.db.session.commit()
        return bookmark_id

    def get_blog(self, bookmark_id: int) -> dict:
        """get_blog returns blog related to given bookmark id

        Args:
            bookmark_id (int): id of the bookmark

        Returns:
            dict: searched bookmark
        """
        sql = """
        SELECT BM.id, B.id, BM.user_id, B.title, BM.description, B.creator, B.link, BM.unread, BM.date
        FROM Bookmarks BM
        JOIN Blogs B ON BM.id = B.bookmark_id
        WHERE BM.id=:id
        """
        bookmark = self.db.session.execute(sql, {"id": bookmark_id}).fetchone()
        return {
            "bookmark_id": bookmark[0],
            "blog_id": bookmark[1],
            "user_id": bookmark[2],
            "title": bookmark[3],
            "description": bookmark[4],
            "creator": bookmark[5],
            "link": bookmark[6],
            "unread": bookmark[7],
            "date": bookmark[8]
        }

    def insert_podcast(self, user_id: int, episode_name: str, podcast_name: str,
                       description: str, creator: str, link: str) -> int:
        """insert_podcast is used to add bookmark, which is type of
        podcast into the database

        Args:
            user_id (int): id of the bookmark's owner
            episode_name (str): name of the podcast episode
            podcast_name (str): name of the podcast serie
            description (str): description of the podcast
            creator (str): creator of the podcast
            link (str): url referencing into the podcast

        Returns:
            int: id of the bookmark (references into bookmarks table)
        """
        bookmark_id = self.insert_bookmark(user_id, description)
        sql = """
        INSERT INTO Podcasts
        (bookmark_id, episode_name, podcast_name, creator, link)
        VALUES (:bookmark_id, :episode_name, :podcast_name, :creator, :link)
        """
        values = {
            "bookmark_id": bookmark_id,
            "episode_name": episode_name,
            "podcast_name": podcast_name,
            "creator": creator,
            "link": link
        }
        self.db.session.execute(sql, values)
        self.db.session.commit()
        return bookmark_id

    def get_podcast(self, bookmark_id: int) -> dict:
        """get_podcast returns podcast related to given bookmark id

        Args:
            bookmark_id (int): id of the bookmark

        Returns:
            dict: searched bookmark
        """
        sql = """
        SELECT BM.id, P.id, BM.user_id, P.episode_name, P.podcast_name, BM.description, P.creator, P.link, BM.unread, BM.date
        FROM Bookmarks BM
        JOIN Podcasts P ON BM.id = P.bookmark_id
        WHERE BM.id=:id
        """
        bookmark = self.db.session.execute(sql, {"id": bookmark_id}).fetchone()
        if bookmark is None:
            return None
        return {
            "bookmark_id": bookmark[0],
            "podcast_id": bookmark[1],
            "user_id": bookmark[2],
            "episode_name": bookmark[3],
            "podcast_name": bookmark[4],
            "description": bookmark[5],
            "creator": bookmark[6],
            "link": bookmark[7],
            "unread": bookmark[8],
            "date": bookmark[9]
        }
    
    def edit_podcast(self,podcast_id,bookmark_id,podcast_name,creator,episode,link,description,unread):
        podcast_sql = """
        UPDATE Podcasts
        SET episode_name=:episode, podcast_name=:podcast, creator=:creator, link=:link
        WHERE id=:id
        """
        self.db.session.execute(podcast_sql, {
            "episode": episode,
            "podcast": podcast_name,
            "creator": creator,
            "link": link,
            "id": podcast_id
        })
        bookmark_sql = """
        UPDATE Bookmarks
        SET description=:description, unread=:unread
        WHERE id=:bookmark_id
        """
        self.db.session.execute(bookmark_sql, {
            "description":description,
            "unread":unread,
            "bookmark_id":bookmark_id
        })
        self.db.session.commit()
        


    def insert_scientific_article(self, user_id: int, title: str,
                                  publication_title: str,
                                  description: str, authors: str,
                                  doi: str, year: int,
                                  publisher: str) -> int:
        """insert_scientific_article is used to add bookmark, which is type of
        scientific article into the database

        Args:
            user_id (int): id of the bookmark's owner
            title (str): title of the article
            publication_title (str): name of the publication, where
                                    article is published
            description (str): description of the article
            authors (str): authors of the article
            doi (str): doi of the article
            year (int): publication year of the article
            publisher (str): publisher of the article

        Returns:
            int: id of the bookmark (references into bookmarks table)
        """
        bookmark_id = self.insert_bookmark(user_id, description)
        sql = """
        INSERT INTO Scientific_articles
        (bookmark_id, title, publication_title, authors, doi, year, publisher)
        VALUES (:bookmark_id, :title, :publication_title, :authors, :doi, :year, :publisher)
        """
        values = {
            "bookmark_id": bookmark_id,
            "title": title,
            "publication_title": publication_title,
            "authors": authors,
            "doi": doi,
            "year": year,
            "publisher": publisher
        }
        self.db.session.execute(sql, values)
        self.db.session.commit()
        return bookmark_id

    def get_scientific_article(self, bookmark_id: int) -> dict:
        """get_scientific_article returns scientific article related to
        given bookmark id

        Args:
            bookmark_id (int): id of the bookmark

        Returns:
            dict: searched bookmark
        """
        sql = """
        SELECT BM.id, SA.id, BM.user_id, SA.title, SA.publication_title, BM.description, SA.authors, SA.doi, SA.year, SA.publisher, BM.unread, BM.date
        FROM Bookmarks BM
        JOIN Scientific_articles SA ON BM.id = SA.bookmark_id
        WHERE BM.id=:id
        """
        bookmark = self.db.session.execute(sql, {"id": bookmark_id}).fetchone()
        return {
            "bookmark_id": bookmark[0],
            "scientific_article_id": bookmark[1],
            "user_id": bookmark[2],
            "title": bookmark[3],
            "publication_title": bookmark[4],
            "description": bookmark[5],
            "authors": bookmark[6],
            "doi": bookmark[7],
            "year": bookmark[8],
            "publisher": bookmark[9],
            "unread": bookmark[10],
            "date": bookmark[11]
        }

    def get_all_books(self, user_id):
        sql = """
        SELECT B.bookmark_id, B.title, B.author, BM.description, B.isbn, BM.unread, BM.date
        FROM Books B
        JOIN Bookmarks BM ON BM.id = B.bookmark_id
        WHERE BM.user_id=:id
        """
        books = self.db.session.execute(sql, {"id": user_id}).fetchall()
        return books
