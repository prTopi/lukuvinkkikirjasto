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
    books = db.get_all_books(1)
    tags = tag_repository.get_all_users_marked_tags()
    tags_dict = {}
    for tag in tags:
        if tag.bookmark_id not in tags_dict:
            tags_dict[tag.bookmark_id] = [tag.tag_name]
        else:
            tags_dict[tag.bookmark_id].append(tag.tag_name)
    print(books[0].bookmark_id)
    return render_template("index.html", books=books, tags=tags_dict)

@app.route("/add_bookmark")
def add_bookmark():
    return render_template("add_bookmark.html",tags=tag_repository.get_user_tags())


@app.route("/add", methods=["POST"])
def add():
    book_type = request.form["type"]
    title = request.form["title"]
    description = request.form["description"]
    author = request.form["author"]
    tags = request.form.getlist('tag')
    if book_type == "book":

        isbn = request.form["ISBN"]
        new_bookmark_id = db.insert_book(user_id, title, description, author, isbn)
    elif book_type == "video":
        link = request.form["link"]
        new_bookmark_id = db.insert_video(user_id, title, description, author, link)
    if tags:
        for tag in tags:
            tag_repository.mark_tag_to_bookmark(int(tag),new_bookmark_id)
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
