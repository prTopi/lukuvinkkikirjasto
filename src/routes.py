"""Module containing all routes of the server"""
from app import app
from flask import redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
from secrets import token_hex
import db

app.secret_key = getenv("SECRET")


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
    if hash_value != None:
        if check_password_hash(hash_value[0],password):
            session["user_id"] = db.find_user_id(username)
            session["username"] = username
            session["csrf_token"] = token_hex(16)
            return redirect("/")
    return redirect("/login")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    del session["csrf_token"]
    return redirect("/")

@app.route("/create")
def create():
    return render_template("create.html",error=False)

@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password2"]

    user_id = db.find_user_id(username)
    if user_id != None:
        return render_template("create.html", error="Username taken", user=username)
    if password != password2:
        return render_template("create.html", error="Passwords not identical", user=username)

    password = generate_password_hash(password2)
    db.insert_user(username,password)
    return redirect("/log")

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
        db.insert_book(session["user_id"], title, description, author, isbn)
    elif book_type == "video":
        link = request.form["link"]
        db.insert_video(session["user_id"], title, description, author, link)

    return redirect("/")