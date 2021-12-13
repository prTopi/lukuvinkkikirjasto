"""Module containing all routes of the server"""
from app import app
from flask import redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from isbnlib import is_isbn10, is_isbn13
from os import getenv
from secrets import token_hex
from repositories.tag_repository import TagRepository
from repositories.user_repository import UserRepository
from repositories.bookmark_repository import BookmarkRepository
if getenv("MODE") != "test":
    from db import db

app.secret_key = getenv("SECRET")

if getenv("MODE") != "test":
    tag_repository = TagRepository(db)
    user_repository = UserRepository(db)
    bookmark_repository = BookmarkRepository(db)

    def update_session(username, route="/"):
        session["user_id"] = user_repository.find_user_id(username)
        session["username"] = username
        session["csrf_token"] = token_hex(16)
        return redirect(route)

    @app.route("/")
    def index():
        try:
            bookmarks = bookmark_repository.get_all_bookmarks(
                session["user_id"])
            bookmark_tags = tag_repository.get_all_users_marked_tags(
                session["user_id"])

            tags_dict = {}
            for tag in bookmark_tags:
                if tag.bookmark_id not in tags_dict:
                    tags_dict[tag.bookmark_id] = [tag.tag_name]
                else:
                    tags_dict[tag.bookmark_id].append(tag.tag_name)
            return render_template("index.html",
                bookmarks=bookmarks,
                tags=tags_dict)
        except KeyError:
            bookmarks = None
            bookmark_tags = None
            return render_template("login.html", error="User not logged in")

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/log", methods=["POST"])
    def log():
        username = request.form["username"]
        password = request.form["password"]
        hash_value = user_repository.find_password(username)
        if hash_value is not None:
            if check_password_hash(hash_value[0], password):
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
        password_confirm = request.form["passwordConfirm"]

        user_id = user_repository.find_user_id(username)
        if user_id is not None:
            return render_template("create.html", error="Username taken",
                                   user=username)
        if password != password_confirm:
            return render_template("create.html",
                                   error="Passwords not identical",
                                   user=username)

        password = generate_password_hash(password_confirm)
        user_repository.insert_user(username, password)
        return update_session(username)

    @app.route("/add_bookmark")
    def add_bookmark():
        user_id = session["user_id"]
        return render_template("add_bookmark.html",
                               tags=tag_repository.get_user_tags(user_id))

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
                new_bookmark_id = bookmark_repository.insert_book(
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
            new_bookmark_id = bookmark_repository.insert_video(
                session["user_id"],
                title,
                description,
                author,
                link)

        elif book_type == "blog":
            link = request.form["link"]
            new_bookmark_id = bookmark_repository.insert_blog(
                session["user_id"],
                title,
                description,
                author,
                link)

        elif book_type == "podcast":
            link = request.form["link"]
            episode_name = request.form["episode"]
            new_bookmark_id = bookmark_repository.insert_podcast(
                session["user_id"],
                episode_name,
                title,
                description,
                author,
                link)

        elif book_type == "scientific_article":
            pt = request.form["publication_title"]
            doi = request.form["doi"]
            publisher = request.form["publisher"]
            year = request.form["year"]
            new_bookmark_id = bookmark_repository.insert_scientific_article(
                session["user_id"],
                title,
                pt,
                description,
                author,
                doi,
                year,
                publisher)

        if tags_to_add:
            for tag in tags_to_add:
                tag_repository.mark_tag_to_bookmark(
                    session["user_id"], int(tag), new_bookmark_id)
        return redirect("/")

    @app.route("/tag", methods=["POST"])
    def tags():
        tag_name = request.form["new_tag_name"]
        tag_repository.create_new_tag(session["user_id"], tag_name)
        return redirect("/add_bookmark")

    @app.route("/bookmark_tag", methods=["POST"])
    def bookmark_tag():
        tag_id = request.form["tag_id"]
        bookmark_id = request.form["bookmark_id"]
        tag_repository.mark_tag_to_bookmark(
            session["user_id"], tag_id, bookmark_id)
        return redirect("/")

    @app.route("/view/<bookmark_type>/<bookmark_id>")
    def bookmark_view_page(bookmark_type, bookmark_id):
        if bookmark_type == "book":
            book = bookmark_repository.get_book(bookmark_id)
            if book is None:
                return redirect("/")
            elif book["user_id"] == session["user_id"]:
                return render_template("view_book.html",book=book)
            return redirect("/")
        elif bookmark_type == "video":
            video = bookmark_repository.get_video(bookmark_id)
            if video is None:
                return redirect("/")
            if video["user_id"] == session["user_id"]:
                return render_template("view_video.html",video=video)
            return redirect("/")
        elif bookmark_type == "blog":
            blog = bookmark_repository.get_blog(bookmark_id)
            if blog is None:
                return redirect("/")
            elif blog["user_id"] == session["user_id"]:
                return render_template("view_blog.html",blog=blog)
            return redirect("/")
        elif bookmark_type == "podcast":
            podcast = bookmark_repository.get_podcast(bookmark_id)
            if podcast is None:
                return redirect("/")
            if podcast["user_id"] == session["user_id"]:
                return render_template("view_podcast.html",podcast=podcast)
            return redirect("/")
        elif bookmark_type == "article":
            article = bookmark_repository.get_scientific_article(bookmark_id)
            if article is None:
                return redirect("/")
            if article["user_id"] == session["user_id"]:
                return render_template("view_article.html",article=article)
            return redirect("/")
        else:
            return redirect("/")

    @app.route("/edit/<bookmark_type>/<bookmark_id>",methods=["GET"])
    def bookmark_edit_page(bookmark_type, bookmark_id):
        if bookmark_type == "book":
            book = bookmark_repository.get_book(bookmark_id)
            if book is None:
                return redirect("/")
            elif book["user_id"] == session["user_id"]:
                return render_template("edit_book.html",book=book)
            return redirect("/")
        elif bookmark_type == "video":
            video = bookmark_repository.get_video(bookmark_id)
            if video is None:
                return redirect("/")
            elif video["user_id"] == session["user_id"]:
                return render_template("edit_video.html",video=video)
            return redirect("/")
        elif bookmark_type == "blog":
            blog = bookmark_repository.get_blog(bookmark_id)
            if blog is None:
                return redirect("/")
            elif blog["user_id"] == session["user_id"]:
                return render_template("edit_blog.html",blog=blog)
            return redirect("/")
        elif bookmark_type == "podcast":
            podcast = bookmark_repository.get_podcast(bookmark_id)
            if podcast is None:
                return redirect("/")
            elif podcast["user_id"] == session["user_id"]:
                return render_template("edit_podcast.html",podcast=podcast)
            return redirect("/")
        elif bookmark_type == "article":
            article = bookmark_repository.get_scientific_article(bookmark_id)
            if article is None:
                return redirect("/")
            elif article["user_id"] == session["user_id"]:
                return render_template("edit_article.html",article=article)
            return redirect("/")
        return redirect("/")

    @app.route("/edit-bookmark",methods=["POST"])
    def edit_bookmark():
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        bookmark_type = request.form["bookmark_type"]
        if bookmark_type == "book":
            book_id = request.form["book_id"]
            bookmark_id = request.form["bookmark_id"]
            book_to_edit = bookmark_repository.get_book(bookmark_id)
            if book_to_edit is None:
                return redirect("/")
            elif book_to_edit["user_id"] == session["user_id"]:
                unread = bool(request.form["Unread"] == "0")
                title = request.form["title"]
                author = request.form["author"]
                isbn = request.form["isbn"]
                description = request.form["description"]
                bookmark_repository.edit_book(
                    book_id,
                    bookmark_id,
                    title,
                    author,
                    isbn,
                    description,
                    unread)
        elif bookmark_type == "video":
            video_id = request.form["video_id"]
            bookmark_id = request.form["bookmark_id"]
            video_to_edit = bookmark_repository.get_video(bookmark_id)
            if video_to_edit is None:
                return redirect("/")
            elif video_to_edit["user_id"] == session["user_id"]:
                unread = bool(request.form["Unread"] == "0")
                title = request.form["title"]
                creator = request.form["creator"]
                link = request.form["link"]
                description = request.form["description"]
                bookmark_repository.edit_video(
                    video_id,
                    bookmark_id,
                    title,
                    creator,
                    link,
                    description,
                    unread)

        elif bookmark_type == "blog":
            blog_id = request.form["blog_id"]
            bookmark_id = request.form["bookmark_id"]
            blog_to_edit = bookmark_repository.get_blog(bookmark_id)
            if blog_to_edit is None:
                return redirect("/")
            elif blog_to_edit["user_id"] == session["user_id"]:
                unread = bool(request.form["Unread"] == "0")
                title = request.form["title"]
                creator = request.form["creator"]
                link = request.form["link"]
                description = request.form["description"]
                bookmark_repository.edit_blog(
                    blog_id,
                    bookmark_id,
                    title,
                    creator,
                    link,
                    description,
                    unread)

        elif bookmark_type == "podcast":
            podcast_id = request.form["podcast_id"]
            bookmark_id = request.form["bookmark_id"]
            podcast_to_edit = bookmark_repository.get_podcast(bookmark_id)
            if podcast_to_edit is None:
                return redirect("/")
            elif podcast_to_edit["user_id"] == session["user_id"]:
                unread = bool(request.form["Unread"] == "0")
                name = request.form["name"]
                creator = request.form["creator"]
                episode = request.form["episode"]
                link = request.form["link"]
                description = request.form["description"]
                bookmark_repository.edit_podcast(
                    podcast_id,
                    bookmark_id,
                    name,
                    creator,
                    episode,
                    link,
                    description,
                    unread)
        elif bookmark_type == "article":
            scientific_article_id = request.form["scientific_article_id"]
            bookmark_id = request.form["bookmark_id"]
            article_to_edit = bookmark_repository.get_scientific_article(
                                                    bookmark_id)
            if article_to_edit is None:
                return redirect("/")
            elif article_to_edit["user_id"] == session["user_id"]:
                unread = bool(request.form["Unread"] == "0")
                title = request.form["title"]
                authors = request.form["authors"]
                publication_title = request.form["publication_title"]
                doi = request.form["doi"]
                year = request.form["year"]
                publisher = request.form["publisher"]
                description = request.form["description"]
                bookmark_id = article_to_edit["bookmark_id"]
                bookmark_repository.edit_scientific_article(
                    scientific_article_id,
                    bookmark_id,
                    title,
                    authors,
                    publication_title,
                    doi,
                    year,
                    publisher,
                    description,
                    unread)
        return redirect("/")

    @app.route("/delete",methods=["POST"])
    def delete_bookmark():
        bookmark_type = request.form["bookmark_type"]
        if bookmark_type == "book":
            pass
        elif bookmark_type == "video":
            pass
        elif bookmark_type == "blog":
            pass
        elif bookmark_type == "podcast":
            pass
        elif bookmark_type == "scientific_article":
            pass
        return redirect("/")
