"""Module containing all routes of the server"""
from app import app
from flask import redirect, render_template, request
from os import getenv
import db

app.secret_key = getenv("SECRET")

user_id = 1


@app.route("/")
def index():
    return render_template("index.html", books=db.get_all_books(1))


@app.route("/add_bookmark")
def add_bookmark():
    return render_template("add_bookmark.html")


@app.route("/add", methods=["POST"])
def add():
    book_type = request.form["type"]
    title = request.form["title"]
    description = request.form["description"]
    author = request.form["author"]
    if book_type == "book":

        isbn = request.form["ISBN"]
        db.insert_book(user_id, title, description, author, isbn)
    elif book_type == "video":
        link = request.form["link"]
        db.insert_video(user_id, title, description, author, link)

    return redirect("/")
