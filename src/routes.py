"""Module containing all routes of the server"""
from app import app
from flask import redirect, render_template, request
from os import getenv
import db
from repositories.tag_repository import TagRepository

app.secret_key = getenv("SECRET")

user_id = 1
tag_repository = TagRepository(1)

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

@app.route("/tag",methods=["POST","GET"])
def tags():
    if request.method == "POST":
        tag_name = request.form["tag_name"]
        tag_repository.create_new_tag(tag_name)
        return redirect("/")
    elif request.method == "GET":
        tags = tag_repository.get_user_tags()
        print(tags)
        return redirect("/")


@app.route("/bookmark_tag", methods=["POST","GET"])
def bookmark_tag():
    if request.method == "POST":
        tag_id = request.form["tag_id"]
        bookmark_id = request.form['bookmark_id']
        tag_repository.mark_tag_to_bookmark(tag_id,bookmark_id)
        return redirect("/")
    elif request.method == "GET":
        bookmark_tags = tag_repository.get_all_users_marked_tags()
        print(bookmark_tags)
        return redirect("/")
