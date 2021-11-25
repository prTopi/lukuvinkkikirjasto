from app import app
from flask import redirect, render_template, request, session, abort
from os import getenv
import db
from secrets import token_hex

app.secret_key = getenv("SECRET")

session["csrf_token"] = token_hex(16)
session["username"] = "Pekka"
session["id"] = 1

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_bookmark/<type>")
def add_bookmark(type):
    if type == "book":
        return render_template("add_book.html")
    if type == "youtube":
        return render_template("add_youtube.html")
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    user_id = session["id"]
    type = request.form["type"]
    name = request.form["name"].strip()

    if type == "book":
        author = request.form["author"]
        ISBN = request.form["ISBN"]
        db.insert_book(name,author,ISBN,user_id)

    if type == "youtube":
        creator = request.form["creator"]
        link = request.form["link"]
        db.insert_video(name,creator,link,user_id)

    return redirect("/")
