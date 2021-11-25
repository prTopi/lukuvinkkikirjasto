from app import app
from sqlalchemy.sql import text
from db import db

class Books():
    @staticmethod
    def get_all_books():

        '''Gets all the books. For MVP only, pls'''

        stmt = text("SELECT * FROM books")
        res = db.engine.execute(stmt)

        return res