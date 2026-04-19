import flask

from . import db_session
from .books import Book
from flask_restful import reqparse, abort, Api, Resource


def abort_if_book_not_found(book_id):
    session = db_session.create_session()
    books = session.query(Book).get(book_id)
    if not books:
        abort(404, message=f"Book {book_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('namebook', required=True)
parser.add_argument('name_author', required=True)
parser.add_argument('isbn', required=True, type=str)
parser.add_argument('yep', required=True, type=int)
parser.add_argument('taken', required=True, type=bool)
parser.add_argument('tbw', required=True, type=str)


class BookResourse(Resource):    
    def get(self, book_id):
        abort_if_book_not_found(book_id)
        session = db_session.create_session()
        books = session.get(Book, book_id)
        return flask.jsonify({'books': books.to_dict(only=('name_book', 'name_author', 'isbn', 'yep', 'taken', 'tbw'))})

    def delete(self, book_id):
        abort_if_book_not_found(book_id)
        session = db_session.create_session()
        book = session.get(Book, book_id)
        session.delete(book)
        session.commit()
        return flask.jsonify({"sucsess": "OK"})
    

class BookListResource(Resource):
    def get(self):
        session = db_session.create_session()
        books = session.query(Book).all()
        return flask.jsonify({"books": [item.to_dict(only=("name_book", "name_author", "isbn", "yep", "taken", "tbw")) for item in books]})
    
    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        book = Book(
            name_book=args['namebook'],
            name_author=args['name_author'],
            isbn=args['isbn'],
            yep=args['yep'],
            taken=args['taken']
        )

        db_sess.add(book)
        db_sess.commit()
        return flask.jsonify({'if': book.id})