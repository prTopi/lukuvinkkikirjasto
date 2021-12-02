"""Handles transactions with the database"""
from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv


app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


def find_user_id(username):
    sql = "SELECT id FROM Users WHERE username=:username"
    try:
        return db.session.execute(sql, {"username": username}).fetchone()[0]
    except (IndexError, TypeError):
        return None


def find_password(username):
    sql = "SELECT password FROM Users WHERE username=:username"
    return db.session.execute(sql, {"username": username}).fetchone()


def insert_user(username, password):
    sql = """
    INSERT INTO Users (username, password)
    VALUES (:username, :password)
    """
    db.session.execute(sql, {"username": username, "password": password})
    db.session.commit()


def insert_bookmark(user_id: int, description: str) -> int:
    """insert_bookmark is used to add basic info of any type into the database
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
    bookmark_id = db.session.execute(sql, values).fetchone()[0]
    return bookmark_id


def insert_book(user_id: int, title: str, description: str, author: str, isbn: str) -> int:
    """insert_book is used to add bookmark, which is type of book into the database

    Args:
        user_id (int): id of the bookmark's owner
        title (str): title of the book
        description (str): description of the book
        author (str): author(s) of the book
        isbn (str): isbn code of the book

    Returns:
        int: id of the bookmark (references into bookmarks table)
    """
    bookmark_id = insert_bookmark(user_id, description)
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
    db.session.execute(sql, values)
    db.session.commit()
    return bookmark_id


def insert_video(user_id: int, title: str, description: str, creator: str, link: str) -> int:
    """insert_video is used to add bookmark, which is type of video into the database

    Args:
        user_id (int): id of the bookmark's owner
        title (str): title of the video
        description (str): description of the video
        creator (str): creator of the video
        link (str): url referencing into the video

    Returns:
        int: id of the bookmark (references into bookmarks table)
    """
    bookmark_id = insert_bookmark(user_id, description)
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
    db.session.execute(sql, values)
    db.session.commit()
    return bookmark_id


def insert_blog(user_id: int, title: str, description: str, creator: str, link: str) -> int:
    """insert_blog is used to add bookmark, which is type of blog into the database

    Args:
        user_id (int): id of the bookmark's owner
        title (str): title of the blog
        description (str): description of the blog
        creator (str): creator of the blog
        link (str): url referencing into the blog

    Returns:
        int: id of the bookmark (references into bookmarks table)
    """
    bookmark_id = insert_bookmark(user_id, description)
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
    db.session.execute(sql, values)
    db.session.commit()
    return bookmark_id


def insert_podcast(user_id: int, episode_name: str, podcast_name: str, description: str, creator: str, link: str) -> int:
    """insert_podcast is used to add bookmark, which is type of podcast into the database

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
    bookmark_id = insert_bookmark(user_id, description)
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
    db.session.execute(sql, values)
    db.session.commit()
    return bookmark_id


def insert_scientific_article(user_id: int, title: str, publication_title: str, description: str, authors: str, doi: str, year: int, publisher: str) -> int:
    """insert_scientific_article is used to add bookmark, which is type of scientific article into the database

    Args:
        user_id (int): id of the bookmark's owner
        title (str): title of the article
        publication_title (str): name of the publication, where article is published
        description (str): description of the article
        authors (str): authors of the article
        doi (str): doi of the article
        year (int): publication year of the article
        publisher (str): publisher of the article

    Returns:
        int: id of the bookmark (references into bookmarks table)
    """
    bookmark_id = insert_bookmark(user_id, description)
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
    db.session.execute(sql, values)
    db.session.commit()
    return bookmark_id


def get_all_books(user_id):
    sql = """
    SELECT B.bookmark_id, B.title, B.author, BM.description, B.isbn, BM.unread, BM.date
    FROM Books B
    JOIN Bookmarks BM ON BM.id = B.bookmark_id
    WHERE BM.user_id=:id
    """
    books = db.session.execute(sql, {"id": user_id}).fetchall()
    return books


def add_new_tag(user_id, tag_name):
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
    db.session.execute(sql, values)
    db.session.commit()


def mark_tag_to_bookmark(tag_id, user_id, bookmark_id):
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
    db.session.execute(sql, values)
    db.session.commit()


def get_all_user_tags(user_id):
    sql = """
    SELECT id, user_id, tag_name
    FROM Tags
    WHERE user_id =:user_id
    """
    values = {
        "user_id": user_id
    }
    tags = db.session.execute(sql, values).fetchall()
    return tags


def get_all_users_marked_tags(user_id):
    sql = """
    SELECT BT.tag_id, BT.user_id, BT.bookmark_id, T.tag_name
    FROM Bookmarks_tags BT
    JOIN Tags T ON T.id = BT.tag_id
    WHERE BT.user_id=:user_id

    """
    values = {
        "user_id": user_id
    }
    marked_tags = db.session.execute(sql, values).fetchall()
    return marked_tags
