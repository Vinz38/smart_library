import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    middlename = sqlalchemy.Column(sqlalchemy.String, nullable=True) 
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    class_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    book_list = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)
    textbook_list = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)
    

    
