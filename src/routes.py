"""Module containing all routes of the server"""
from app import app
from flask import redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from isbnlib import is_isbn10, is_isbn13
from os import getenv
from secrets import token_hex
import db

app.secret_key = getenv("SECRET")


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
    return render_template("index.html", books=books)

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
    return redirect("/login")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    del session["csrf_token"]
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
    return render_template("add_bookmark.html")


@app.route("/add", methods=["POST"])
def add():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    book_type = request.form["type"]
    title = request.form["title"]
    description = request.form["description"]
    author = request.form["author"]
    if book_type == "book":
        isbn = request.form["ISBN"]
        if is_isbn10(isbn) or is_isbn13(isbn):
            db.insert_book(session["user_id"], title, description, author, isbn)
        else:
            return render_template("add_bookmark.html", title=title,
                                   description=description, author=author,
                                   isbn=isbn, error="Invalid ISBN")
    elif book_type == "video":
        link = request.form["link"]
        db.insert_video(session["user_id"], title, description, author, link)

    return redirect("/")
