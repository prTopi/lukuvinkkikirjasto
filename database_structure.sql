CREATE TABLE Users (id SERIAL PRIMARY KEY, username TEXT NOT NULL, password TEXT);

CREATE TABLE Bookmarks (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES Users, description TEXT, unread BOOLEAN DEFAULT false, date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE Books (id SERIAL PRIMARY KEY, bookmark_id INTEGER NOT NULL REFERENCES Bookmarks, title TEXT, author TEXT, ISBN TEXT);

CREATE TABLE Videos (id SERIAL PRIMARY KEY, bookmark_id INTEGER NOT NULL REFERENCES Bookmarks, title TEXT, creator TEXT, link TEXT);

CREATE TABLE Blogs (id SERIAL PRIMARY KEY, bookmark_id INTEGER NOT NULL REFERENCES Bookmarks, title TEXT, creator TEXT, link TEXT);

CREATE TABLE Podcasts (id SERIAL PRIMARY KEY, bookmark_id INTEGER NOT NULL REFERENCES Bookmarks, episode_name TEXT, podcast_name TEXT, creator TEXT, link TEXT);

CREATE TABLE ScientificArticles (id SERIAL PRIMARY KEY, bookmark_id INTEGER NOT NULL REFERENCES Bookmarks, title TEXT, publication_title TEXT, authors TEXT, doi TEXT, year INTEGER, publisher TEXT);

INSERT INTO Users (username, password) VALUES ('testi', 'pbkdf2:sha256:260000$A4StfLh8tPdGZXYF$c78a1cad4deccf8ae031456bfa443d2dcb92d3b03021b9cfe1fb71be08615619');
