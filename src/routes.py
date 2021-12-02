"""Module containing all routes of the server"""
from app import app
from flask import redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from isbnlib import is_isbn10, is_isbn13
from os import getenv
from secrets import token_hex
import db
from repositories.tag_repository import TagRepository

app.secret_key = getenv("SECRET")
tag_repository = TagRepository(1)


def update_session(username, route="/"):
    session["user_id"] = db.find_user_id(username)
    session["username"] = username
    session["csrf_token"] = token_hex(16)
    return redirect(route)

@app.route("/")
def index():
    try:
        books = db.get_all_books(session["user_id"])
    except KeyError:
        books = None
    bookmark_tags = tag_repository.get_all_users_marked_tags()
    tags_dict = {}
    for tag in bookmark_tags:
        if tag.bookmark_id not in tags_dict:
            tags_dict[tag.bookmark_id] = [tag.tag_name]
        else:
            tags_dict[tag.bookmark_id].append(tag.tag_name)
    return render_template("index.html", books=books, tags=tags_dict)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/log", methods=["POST"])
def log():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = db.find_password(username)
    if hash_value is not None:
        if check_password_hash(hash_value[0],password):
            return update_session(username)
    return render_template("login.html",
                           error="Username and password not matching")

@app.route("/logout")
def logout():
    try:
        del session["user_id"]
        del session["username"]
        del session["csrf_token"]
    except KeyError:
        pass
    return redirect("/")

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password2"]

    user_id = db.find_user_id(username)
    if user_id is not None:
        return render_template("create.html", error="Username taken",
                               user=username)
    if password != password2:
        return render_template("create.html", error="Passwords not identical",
                               user=username)

    password = generate_password_hash(password2)
    db.insert_user(username, password)
    return update_session(username)

@app.route("/add_bookmark")
def add_bookmark():
    return render_template("add_bookmark.html",
    tags=tag_repository.get_user_tags())


@app.route("/add", methods=["POST"])
def add():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    book_type = request.form["type"]
    title = request.form["title"]
    description = request.form["description"]
    author = request.form["author"]
    tags_to_add = request.form.getlist("tag")
    if book_type == "book":
        isbn = request.form["ISBN"]
        if is_isbn10(isbn) or is_isbn13(isbn):
            new_bookmark_id = db.insert_book(
                session["user_id"],
                title,
                description,
                author,
                isbn
            )
        else:
            return render_template("add_bookmark.html", title=title,
                                   description=description, author=author,
                                   isbn=isbn, error="Invalid ISBN")
    elif book_type == "video":
        link = request.form["link"]
        new_bookmark_id = db.insert_video(
            session["user_id"],
            title,
            description,
            author,
            link)
    if tags_to_add:
        for tag in tags_to_add:
            tag_repository.mark_tag_to_bookmark(int(tag),new_bookmark_id)
    return redirect("/")

@app.route("/tag",methods=["POST"])
def tags():
    tag_name = request.form["new_tag_name"]
    tag_repository.create_new_tag(tag_name)
    return redirect("/add_bookmark")

@app.route("/bookmark_tag", methods=["POST"])
def bookmark_tag():
    tag_id = request.form["tag_id"]
    bookmark_id = request.form["bookmark_id"]
    tag_repository.mark_tag_to_bookmark(tag_id,bookmark_id)
    return redirect("/")
