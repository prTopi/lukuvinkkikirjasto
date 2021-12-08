"""Handles transactions with the database"""
from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv


app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
