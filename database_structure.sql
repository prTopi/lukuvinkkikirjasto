CREATE TABLE Users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE Books (id SERIAL PRIMARY KEY, bookmark_id INTEGER REFERENCES Bookmarks, title TEXT, author TEXT, ISBN TEXT);
CREATE TABLE Videos (id SERIAL PRIMARY KEY, bookmark_id INTEGER REFERENCES Bookmarks, title TEXT, creator TEXT, link TEXT);
CREATE TABLE Blogs (id SERIAL PRIMARY KEY, bookmark_id INTEGER REFERENCES Bookmarks, title TEXT, creator TEXT, link TEXT);
CREATE TABLE Podcasts (id SERIAL PRIMARY KEY, bookmark_id INTEGER REFERENCES Bookmarks, title TEXT, creator TEXT, link TEXT);
CREATE TABLE Bookmarks (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES Users, description TEXT, unread BOOLEAN, date DATE);
