"""Handles transactions with the database"""
from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv


app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


def insert_bookmark(user_id, description):
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


def insert_book(user_id, title, description, author, isbn):
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


def insert_video(user_id, title, description, creator, link):
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


def get_all_books(user_id):
    sql = """
    SELECT B.title, B.author, BM.description, B.isbn, BM.unread, BM.date
    FROM Books B
    JOIN Bookmarks BM ON BM.id = B.bookmark_id
    WHERE BM.user_id=:id
    """
    books = db.session.execute(sql, {"id": user_id}).fetchall()
    return books
