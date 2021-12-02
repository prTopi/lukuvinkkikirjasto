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
        return db.session.execute(sql, {"username":username}).fetchone()[0]
    except (IndexError, TypeError):
        return None

def find_password(username):
    sql = "SELECT password FROM Users WHERE username=:username"
    return db.session.execute(sql, {"username":username}).fetchone()

def insert_user(username,password):
    sql = """
    INSERT INTO Users (username, password)
    VALUES (:username, :password)
    """
    db.session.execute(sql, {"username":username,"password":password})
    db.session.commit()


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
    return bookmark_id


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

def add_new_tag(user_id,tag_name):
    sql = """
    INSERT INTO Tags
    (user_id, tag_name)
    VALUES
    (:user_id,:tag_name)
    """
    values = {
        "user_id":user_id,
        "tag_name":tag_name
    }
    db.session.execute(sql,values)
    db.session.commit()

def mark_tag_to_bookmark(tag_id,user_id,bookmark_id):
    sql = """
    INSERT INTO Bookmarks_tags
    (tag_id, user_id, bookmark_id)
    VALUES
    (:tag_id, :user_id, :bookmark_id)
    """
    values = {
        "tag_id":tag_id,
        "user_id":user_id,
        "bookmark_id":bookmark_id
    }
    db.session.execute(sql,values)
    db.session.commit()

def get_all_user_tags(user_id):
    sql = """
    SELECT id, user_id, tag_name
    FROM Tags
    WHERE user_id =:user_id
    """
    values = {
        "user_id":user_id
    }
    tags = db.session.execute(sql,values).fetchall()
    return tags

def get_all_users_marked_tags(user_id):
    sql = """
    SELECT BT.tag_id, BT.user_id, BT.bookmark_id, T.tag_name
    FROM Bookmarks_tags BT
    JOIN Tags T ON T.id = BT.tag_id
    WHERE BT.user_id=:user_id

    """
    values = {
        "user_id":user_id
    }
    marked_tags = db.session.execute(sql,values).fetchall()
    return marked_tags
