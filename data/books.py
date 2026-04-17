import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Book(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_book = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name_author = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    isbn = sqlalchemy.Column(
        sqlalchemy.String, nullable=False, unique=True)
    yep = sqlalchemy.Column(
        sqlalchemy.Integer, nullable=False)  #! yearofpublication
    taken = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    tbw = sqlalchemy.Column(sqlalchemy.String, default="-", nullable=True) #! taken by whom
