import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class TextBook(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'textbooks'

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, autoincrement=True)
    itemtype = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    textbookname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    yearofpublication = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    

    
