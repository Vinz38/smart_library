import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class TextBook(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'textbooks'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    itemtype = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    id_book = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True)
    tbn = sqlalchemy.Column(
        sqlalchemy.String, nullable=False)  #! textbookname
    yep = sqlalchemy.Column(sqlalchemy.Integer, nullable=False) #! yearofpublication
    authors_list = sqlalchemy.Column(sqlalchemy.String, nullable=False)
