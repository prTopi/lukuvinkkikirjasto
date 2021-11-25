from app import app
from flask import redirect, render_template, request
from os import getenv
import db
from secrets import token_hex

app.secret_key = getenv("SECRET")

user_id = 1


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_bookmark")
def add_bookmark():
    return render_template("add_bookmark.html")


@app.route("/add", methods=["POST"])
def add():
    type = request.form["type"]
    name = request.form["title"].strip()
    title = request.form["title"]
    description = request.form["description"]
    author = request.form["author"]
    if type == "book":

        isbn = request.form["ISBN"]
        db.insert_book(user_id, title, description, author, isbn)
    elif type == "video":
        link = request.form["link"]
        db.insert_video(user_id, title, description, author, link)

    return redirect("/")
