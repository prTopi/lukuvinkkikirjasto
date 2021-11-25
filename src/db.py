from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv


app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
db = SQLAlchemy(app)

def insert_book(name,author,ISBN,user_id):
    db.session.execute("INSERT INTO Books (user_id, name, author, ISBN) VALUES (:user_id, :name, :author, :ISBN)", {"user_id":user_id,"name":name,"author":author,"ISBN":ISBN})
    db.session.commit()

def insert_video(name,creator,link,user_id):
    db.session.execute("INSERT INTO Videos (user_id, name, creator, link) VALUES (:user_id, :name, :creator, :link)", {"user_id":user_id,"name":name,"creator":creator,"link":link})
    db.session.commit()